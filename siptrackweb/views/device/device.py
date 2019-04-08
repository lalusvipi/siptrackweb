import re

from django.http import HttpResponse
import siptracklib.errors
import json
import time

from siptrackweb.views import helpers
from siptrackweb.views import attribute
from siptrackweb.views import config
from siptrackweb.views.device.utils import make_device_association_list
import category
from siptrackweb.forms import *

import siptracklib.template

class RackUnit(object):
    def __init__(self, device = None, unit = None):
        self.device = device
        self.linked_device = None
        self.selected = False
        self.reserved = False
        self.occupied = False
        if device:
            try:
                self.unit = int(device.attributes.get('name'))
            except ValueError:
                self.unit = 0
            assoc = device.listLinks()
            if assoc:
                self.empty = False
                self.linked_device = assoc[0]
                self.name = self.linked_device.attributes.get('name')
            else:
                self.empty = True
                self.name = ''
            if device.attributes.get('rack_unit_reserved'):
                self.reserved = True
                self.empty = False
            if device.attributes.get('rack_unit_occupied'):
                self.occupied = True
                self.empty = False
        else:
            self.unit = unit
            self.empty = True
            self.name = ''
        self.unit_str = '%02d' % (self.unit)
        self.all_units = [self.unit_str]

    def __str__(self):
        return '<RackUnit %d>' % self.unit

    def __cmp__(self, other):
        return cmp(self.unit, other.unit)

    def mergeUnit(self, unit):
        self.all_units.append(unit.unit_str)


class DeviceRack(object):
    def __init__(self, device, highlight_device = None):
        self.device = device
        self.highlight_device = highlight_device
        self.units = self._makeUnits()

    def _makeUnits(self):
        units = [RackUnit(d) for d in self.device.listChildren(include=['device']) if d.attributes.get('class') == 'rack unit']
        if not units:
            units = [RackUnit(None, 42)]
        units.sort()
        missing = []
        pos = 1
        for unit in units:
            while pos < unit.unit:
                missing.append(RackUnit(unit=pos))
                pos += 1
            pos += 1
        units += missing
        units.sort()
        units.reverse()
        prev = None
        prev_merge = None
        remove = []
        for unit in units:
            if unit.reserved or unit.occupied:
                prev_merge = None
                continue
            if prev and unit.linked_device == prev.linked_device:
                if prev_merge and unit.linked_device == prev_merge.linked_device:
                    prev_merge.mergeUnit(unit)
                else:
                    prev.mergeUnit(unit)
                    prev_merge = prev
                remove.append(unit)
            else:
                prev_merge = None
            prev = unit
            if self.highlight_device and unit.linked_device == self.highlight_device:
                unit.selected = True
        for unit in remove:
            units.remove(unit)
        return units

def make_device_rack(device):
    if device.attributes.get('class') == 'rack':
        return DeviceRack(device)
    else:
        for assoc in device.listLinks(include=['device']):
            if assoc.attributes.get('class') == 'rack unit':
                return DeviceRack(assoc.parent, device)
            if assoc.attributes.get('class') == 'rack':
                return DeviceRack(assoc, device)
    return None

def make_device_list_with_links(parent):
    ret = []
    for device in parent.listChildren(include = ['device']):
        ret.append(device)
        device.links = make_device_association_list(device)
    return ret

@helpers.authcheck
def index(request, view_oid):
    pm = helpers.PageManager(request, '')
    pm.section('device')
    view = pm.object_store.getOID(view_oid)
    device_tree = view.getChildByName('default', include = ['device tree'])
    return category.display(request, pm, device_tree)

@helpers.authcheck
def display(request, oid):
    pm = helpers.PageManager(request, '')
    device = pm.object_store.getOID(oid)
    if device.class_name == 'device':
        return display_device(request, pm, device)
    else:
        return category.display(request, pm, device)

@helpers.authcheck
def display_device(request, pm, device):
    pm.render_path = 'stweb/views/devices/display.html'
    pm.render_var['device'] = device
    pm.setVar('device_tree', device.getDeviceTree())
    pm.render_var['device_list'] = make_device_list_with_links(device)
    sort_method = device.attributes.get('web-device-sort-method')
    if sort_method == 'reverse':
        pm.render_var['device_list'].reverse()
    elif sort_method == 'letter-number':
        pm.render_var['device_list'].sort(cmp = helpers.device_letter_number_sorter)
    else:
        pass
    if device.attributes.get('reverse-device-sort-order', False):
        pm.render_var['device_list'].reverse()
    pm.render_var['password_list'] = device.listChildren(include = ['password'])
    pm.render_var['attribute_list'] = attribute.parse_attributes(device)
    pm.render_var['config_list'] = config.parse_config(device)
    pm.render_var['permission_list'] = device.listChildren(include = ['permission'])
    pm.render_var['device_config_list'] = device.listChildren(include = ['device config'])
    for device_config in pm.render_var['device_config_list']:
        device_config.stats = device_config.getStats()
        if device_config.stats['latest_timestamp']:
            device_config.stats['pretty_latest_timestamp'] = time.ctime(device_config.stats['latest_timestamp'])
        else:
            device_config.stats['pretty_latest_timestamp'] = 'Nothing received'
    pm.render_var['device_config_template_list'] = device.listChildren(include = ['device config template'])
    pm.render_var['event_log_list'] = device.listChildren(include = ['event log'])
    pm.render_var['event_log_list'].sort(cmp=lambda x, y: cmp(x.ctime, y.ctime))

    if 'assigned network' in request.session:
        pm.render_var['assigned_network'] = request.session['assigned network']
        del request.session['assigned network']
    networks = device.listNetworks()
    hosts = [n for n in networks if n.isHost()]
    subnets = [n for n in networks if not n.isHost()]
    pm.render_var['network_host_list'] = hosts
    pm.render_var['network_subnet_list'] = subnets
    pm.render_var['interface_network_host_list'] = device.listInterfaceNetworks()
    assoc_list = make_device_association_list(device)
    pm.render_var['device_association_list'] = assoc_list
    pm.render_var['device_rack'] = make_device_rack(device)
    
    device_password_assoc = {
        'all': device.listAssociations(
            include=['password', 'password category']
        )
    }
    device_password_assoc['categories'] = [i for i in device_password_assoc['all'] if i.class_id == 'PC']
    device_password_assoc['passwords'] = [i for i in device_password_assoc['all'] if i.class_id == 'P']
    pm.render_var['device_password_associations'] = device_password_assoc

    pm.render_var['primary_network'] = None
    pm.render_var['default_gateway_guessed'] = True
    if len(hosts) == 1:
        pm.render_var['primary_network'] = hosts[0]
    else:
        for host in hosts:
            if not host.attributes.get('secondary'):
                if pm.render_var['primary_network']:
                    pm.render_var['primary_network'] = None
                    break
                pm.render_var['primary_network'] = host
    if pm.render_var['primary_network']:
        host = pm.render_var['primary_network']
        if host.parent.class_id == host.class_id:
            parent = host.parent
            gateway = None
            for net in parent.listNetworks():
                if net.attributes.get('gateway'):
                    pm.render_var['default_gateway_guessed'] = False
                    gateway = net
                    break
            if parent.class_name == 'ipv4 network':
                if not gateway:
                    pm.render_var['default_gateway'] = parent.address.inc().strAddress()
                else:
                    pm.render_var['default_gateway'] = gateway.address.strAddress()
            elif parent.class_name == 'ipv6 network':
                if gateway:
                    pm.render_var['default_gateway'] = gateway.address.first
                else:
                    pm.render_var['default_gateway'] = parent.address.first
            else:
                pm.render_var['primary_network'] = None
        else:
            pm.render_var['primary_network'] = None


    if pm.tagged_oid and pm.tagged_oid.oid != device.oid and \
            pm.tagged_oid.class_name == 'device':
        pm.render_var['valid_tag_target'] = True

    if pm.tagged_oid and pm.tagged_oid.oid != device.oid and \
            pm.tagged_oid.class_name in ['device category', 'device tree']:
        pm.render_var['valid_copy_target'] = True

    pm.path(device)

    return pm.render()

@helpers.authcheck
def delete(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    url = '/device/delete/post/%s/' % (device.oid)
    pm.addForm(DeleteForm(), url,
            'remove device', message = 'Removing device.')
    pm.path(device)

    return pm.render()

@helpers.authcheck
def delete_post(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)
    url = '/device/delete/post/%s/' % (device.oid)
    pm.addForm(DeleteForm(request.POST), url,
            'remove device', message = 'Removing device.')
    if not pm.form.is_valid():
        return pm.render()

    parent_oid = device.parent.oid
    device.delete()

    return pm.redirect('device.display', (parent_oid,))

@helpers.authcheck
def add_template_select(request, parent_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    parent = pm.setVar('parent', pm.object_store.getOID(parent_oid))
    pm.path(parent)

    templates = [template for template in \
            siptracklib.template.suggest_templates(parent, 'device template')
            if template.attributes.get('device_creation', False) and \
            not template.inheritance_only]
    url = '/device/add/template/set/%s/' % (parent_oid)
    pm.addForm(TemplateSelectForm(templates, True), url, 'create device')
    return pm.render()

@helpers.authcheck
def add_template_set(request, parent_oid):
    pm = helpers.PageManager(request, 'stweb/templates/apply_set.html')
    parent = pm.setVar('parent', pm.object_store.getOID(parent_oid))
    pm.path(parent)

    templates = [template for template in \
            siptracklib.template.suggest_templates(parent, 'device template')
            if template.attributes.get('device_creation', False)]
    form = TemplateSelectForm(templates, True, request.POST)
    if not form.is_valid():
        url = '/device/add/template/set/%s/' % (parent_oid)
        pm.addForm(form, url, 'create device')
        return pm.render()

    # No template chosen, just create an empty device.
    if form.cleaned_data['template'] == '-1':
        device = parent.add('device')
        return pm.redirect('device.display', (device.oid,))

    template = pm.object_store.getOID(form.cleaned_data['template'])
    pm.render_var['template'] = template
    url = '/device/add/template/post/%s/%s/' % (parent_oid, template.oid)
    form = TemplateSetForm(template)
    pm.addForm(form, url, 'create device')
    return pm.render()

@helpers.authcheck
def add_template_post(request, parent_oid, template_oid):
    pm = helpers.PageManager(request, 'stweb/templates/apply_set.html')
    parent = pm.setVar('parent', pm.object_store.getOID(parent_oid))
    pm.path(parent)

    template = pm.object_store.getOID(template_oid)
    pm.render_var['template'] = template

    url = '/device/add/template/post/%s/%s/' % (parent_oid, template.oid)
    form = TemplateSetForm(template, request.POST)
    pm.addForm(form, url, 'create device')
    if not pm.form.is_valid():
        return pm.error('')

    apply_rules = []
    for key, value in request.POST.iteritems():
        if not key.startswith('apply-argument'):
            continue
        _, _, rule_oid = key.split('-')
        apply_rules.append(rule_oid)

    arguments = {}
    for key in pm.form.cleaned_data:
        if not key.startswith('argument-'):
            continue
        prefix, rule_oid = key.split('-', 1)
        arguments[rule_oid] = [pm.form.cleaned_data[key]]

    skip_rules = []
    for rule in template.combinedRules():
        if rule.oid not in apply_rules:
            skip_rules.append(rule.oid)
        if rule.apply_arguments == 0 and rule.oid in arguments:
            del arguments[rule.oid]
        if rule.class_name == 'template rule password':
            arguments[rule.oid] = [helpers.generate_password()]
        if rule.class_name == 'template rule subdevice':
            arguments[rule.oid] = [{}, arguments[rule.oid][0]]

    device = parent.add('device')
    overwrite = True
    try:
        template.apply(device, arguments, overwrite, skip_rules)
    except siptracklib.errors.SiptrackError, e:
        device.delete()
        return pm.error(str(e))

    return pm.redirect('device.display', (device.oid,))

@helpers.authcheck
def disable(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    url = '/device/disable/post/%s/' % (device.oid)
    pm.addForm(EmptyForm(), url,
            'disable device', message = 'Disabling device.')
    pm.path(device)

    return pm.render()

@helpers.authcheck
def disable_post(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)
    url = '/device/disable/post/%s/' % (device.oid)
    pm.addForm(EmptyForm(request.POST), url,
            'disable device', message = 'Disabling device.')
    if not pm.form.is_valid():
        return pm.render()

    device.attributes['disabled'] = True

    return pm.redirect('device.display', (oid,))

@helpers.authcheck
def enable(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    url = '/device/enable/post/%s/' % (device.oid)
    pm.addForm(EmptyForm(), url,
            'enable device', message = 'Enabling device.')
    pm.path(device)

    return pm.render()

@helpers.authcheck
def enable_post(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)
    url = '/device/enable/post/%s/' % (device.oid)
    pm.addForm(EmptyForm(request.POST), url,
            'enable device', message = 'Enabling device.')
    if not pm.form.is_valid():
        return pm.render()

    disabled = device.attributes.getObject('disabled')
    if disabled is not None:
        disabled.delete()

    return pm.redirect('device.display', (oid,))

@helpers.authcheck
def recreate_template_select(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)

    templates = [template for template in \
            siptracklib.template.suggest_templates(device, 'device template')
            if template.attributes.get('device_creation', False) and \
            not template.inheritance_only]
    url = '/device/recreate/template/set/%s/' % (oid)
    pm.addForm(TemplateSelectForm(templates, False), url, 're-create device')
    return pm.render()

@helpers.authcheck
def recreate_template_set(request, oid):
    pm = helpers.PageManager(request, 'stweb/templates/apply_set.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)

    templates = [template for template in \
            siptracklib.template.suggest_templates(device, 'device template')
            if template.attributes.get('device_creation', False)]
    form = TemplateSelectForm(templates, False, request.POST)
    if not form.is_valid():
        url = '/device/recreate/template/set/%s/' % (oid)
        pm.addForm(form, url, 're-create device')
        return pm.render()

    template = pm.object_store.getOID(form.cleaned_data['template'])
    pm.render_var['template'] = template
    url = '/device/recreate/template/post/%s/%s/' % (oid, template.oid)
    form = TemplateSetForm(template)
    pm.addForm(form, url, 're-create device')
    return pm.render()

@helpers.authcheck
def recreate_template_post(request, oid, template_oid):
    pm = helpers.PageManager(request, 'stweb/templates/apply_set.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)

    template = pm.object_store.getOID(template_oid)
    pm.render_var['template'] = template

    url = '/device/recreate/template/post/%s/%s/' % (oid, template.oid)
    form = TemplateSetForm(template, request.POST)
    pm.addForm(form, url, 're-create device')
    if not pm.form.is_valid():
        return pm.error('')

    apply_rules = []
    for key, value in request.POST.iteritems():
        if not key.startswith('apply-argument'):
            continue
        _, _, rule_oid = key.split('-')
        apply_rules.append(rule_oid)

    arguments = {}
    for key in pm.form.cleaned_data:
        if not key.startswith('argument-'):
            continue
        prefix, rule_oid = key.split('-', 1)
        arguments[rule_oid] = [pm.form.cleaned_data[key]]

    skip_rules = []
    for rule in template.combinedRules():
        if rule.oid not in apply_rules:
            skip_rules.append(rule.oid)
        if rule.apply_arguments == 0 and rule.oid in arguments:
            del arguments[rule.oid]
        if rule.class_name == 'template rule password':
            arguments[rule.oid] = [helpers.generate_password()]
        if rule.class_name == 'template rule subdevice':
            arguments[rule.oid] = [{}, arguments[rule.oid][0]]

    overwrite = True
    try:
        template.apply(device, arguments, overwrite, skip_rules)
    except siptracklib.errors.SiptrackError, e:
        return pm.error(str(e))

    return pm.redirect('device.display', (device.oid,))

@helpers.authcheck
def copy(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    url = '/device/copy/post/%s/' % (device.oid)
    pm.addForm(DeviceCopyForm(), url,
            'copy device', message = 'Copying device.')
    pm.path(device)

    return pm.render()

@helpers.authcheck
def copy_post(request, oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(oid))
    pm.path(device)
    url = '/device/copy/post/%s/' % (device.oid)
    pm.addForm(DeviceCopyForm(request.POST), url,
            'copy device', message = 'Copying device.')
    if not pm.form.is_valid():
        return pm.render()
    include_nodes = []
    exclude_nodes = []
    include_links = []
    exclude_links = []
    if pm.form.cleaned_data['skip_attributes']:
        exclude_nodes.extend(['attribute', 'versioned attribute'])
    if pm.form.cleaned_data['skip_devices']:
        exclude_nodes.extend(['device'])
    if pm.form.cleaned_data['skip_networks']:
        exclude_links.extend(['ipv4 network', 'ipv6 network'])

    new_device = device.copy(pm.tagged_oid, include_nodes, exclude_nodes, include_links, exclude_links)

    return pm.redirect('device.display', (new_device.oid,))

def export_get_device_path(device):
    ret = []
    while device.class_name == 'device':
        d = {'name': device.attributes.get('name')}
        ret.append(d)
        device = device.parent
    ret.reverse()
    return ret

def export_get_networks(device):
    ret = []
    for network in device.listNetworks():
        ret.append({'oid': network.oid, 'address': str(network), 'secondary': network.attributes.get('secondary', False)})
    return ret

def export_get_device_info(device):
    ret = {'oid': device.oid,
           'name': device.attributes.get('name', ''),
           'class': device.attributes.get('class', ''),
           'path': export_get_device_path(device),
           'networks': export_get_networks(device),
           'disabled': device.attributes.get('disabled', False)}
    return ret

@helpers.authcheck
def export(request, oid):
    pm = helpers.PageManager(request, '')
    node = pm.object_store.getOID(oid)
    data = {'type': node.class_name, 'oid': node.oid, 'attributes': [], 'networks': [], 'subdevices': [], 'devicelinks': [], 'class': node.attributes.get('class')}
    for attr in node.attributes:
        if attr.atype in ['binary']:
            continue
        data['attributes'].append({'name': attr.name, 'value': attr.value, 'type': attr.atype})
    data['networks'] = export_get_networks(node)
    for subdevice in node.listChildren(include = ['device']):
        sd_dict = {'oid': subdevice.oid, 'name': subdevice.attributes.get('name', ''), 'class': subdevice.attributes.get('class', ''), 'devicelinks': []}
        for link in subdevice.listLinks(include = ['device']):
            sd_dict['devicelinks'].append(export_get_device_info(link))
        data['subdevices'].append(sd_dict)
    for link in node.listLinks(include = ['device']):
        data['devicelinks'].append(export_get_device_info(link))
    data = json.dumps(data, sort_keys=True, indent=2)
    filename = '%s.json' % (node.attributes.get('name', node.oid))
    filename = filename.replace(' ', '_').replace(',', '_')
    return pm.renderDownload(data, '%s.json' % (node.attributes.get('name', node.oid)))

@helpers.authcheck
def rack_unit_occupied(request, device_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(device_oid))
    url = '/rack/unit/occupied/post/%s/' % (device.oid)
    pm.addForm(RackUnitOccupiedForm(), url,
               'rack unit occupied')
    pm.path(device)

    return pm.render()

@helpers.authcheck
def rack_unit_occupied_post(request, device_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(device_oid))
    pm.path(device)
    url = '/rack/unit/occupied/post/%s/' % (device.oid)
    pm.addForm(RackUnitOccupiedForm(request.POST), url,
               'rack unit occupied')
    if not pm.form.is_valid():
        return pm.render()

    device.attributes['rack_unit_occupied'] = True
    device.attributes['rack_unit_occupied_reason'] = pm.form.cleaned_data['reason']
    device.attributes['rack_unit_occupied_timestamp'] = int(time.time())

    return pm.redirect('device.display', (device_oid,))

@helpers.authcheck
def rack_unit_unoccupied(request, device_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(device_oid))
    url = '/rack/unit/unoccupied/%s/' % (device.oid)
    pm.path(device)
    if request.method == 'POST':
        pm.addForm(ConfirmForm(request.POST), url,
                   'rack unit unoccupied')
        if pm.form.is_valid():
            device.attributes.getObject('rack_unit_occupied').delete()
            device.attributes.getObject('rack_unit_occupied_reason').delete()
            device.attributes.getObject('rack_unit_occupied_timestamp').delete()
            return pm.redirect('device.display', (device_oid,))
        else:
            raise Exception('invalid')
    else:
        pm.addForm(ConfirmForm(), url,
                   'rack unit unoccupied')
    return pm.render()

@helpers.authcheck
def rack_unit_reserved(request, device_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(device_oid))
    url = '/rack/unit/reserved/post/%s/' % (device.oid)
    pm.addForm(RackUnitReservedForm(), url,
               'rack unit reserved')
    pm.path(device)

    return pm.render()

@helpers.authcheck
def rack_unit_reserved_post(request, device_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(device_oid))
    pm.path(device)
    url = '/rack/unit/reserved/post/%s/' % (device.oid)
    pm.addForm(RackUnitReservedForm(request.POST), url,
               'rack unit reserved')
    if not pm.form.is_valid():
        return pm.render()

    device.attributes['rack_unit_reserved'] = True
    device.attributes['rack_unit_reserved_reason'] = pm.form.cleaned_data['reason']
    device.attributes['rack_unit_reserved_timestamp'] = int(time.time())

    return pm.redirect('device.display', (device_oid,))

@helpers.authcheck
def rack_unit_unreserved(request, device_oid):
    pm = helpers.PageManager(request, 'stweb/generic_form.html')
    device = pm.setVar('device', pm.object_store.getOID(device_oid))
    url = '/rack/unit/unreserved/%s/' % (device.oid)
    pm.path(device)
    if request.method == 'POST':
        pm.addForm(ConfirmForm(request.POST), url,
                   'rack unit unreserved')
        if pm.form.is_valid():
            device.attributes.getObject('rack_unit_reserved').delete()
            device.attributes.getObject('rack_unit_reserved_reason').delete()
            device.attributes.getObject('rack_unit_reserved_timestamp').delete()
            return pm.redirect('device.display', (device_oid,))
        else:
            raise Exception('invalid')
    else:
        pm.addForm(ConfirmForm(), url,
                   'rack unit unreserved')
    return pm.render()
