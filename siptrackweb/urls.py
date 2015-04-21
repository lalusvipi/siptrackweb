try:
    from django.conf.urls.defaults import patterns
except ImportError:
    from django.conf.urls import patterns
from siptrackweb import views

urlpatterns = patterns('siptrackweb.views',
    (r'^$', 'root.index'),

    (r'^display/(?P<oid>[^/]+)/$', 'display.display'),

    (r'^view/$', 'view.index'),
    (r'^view/add/$', 'view.add'),
    (r'^view/add/post/$', 'view.add_post'),
    (r'^view/delete/(?P<oid>[^/]+)/$', 'view.delete'),
    (r'^view/delete/post/(?P<oid>[^/]+)/$', 'view.delete_post'),
    (r'^view/update/(?P<oid>[^/]+)/$', 'view.update'),
    (r'^view/update/post/(?P<oid>[^/]+)/$', 'view.update_post'),
    (r'^view/display/(?P<oid>[^/]+)/$', 'view.display'),

    (r'^attribute/add/select/(?P<target_oid>[^/]+)/$', 'attribute.add_select'),
    (r'^attribute/add/set/(?P<target_oid>[^/]+)/$', 'attribute.add_set'),
    (r'^attribute/add/post/(?P<target_oid>[^/]+)/$', 'attribute.add_post'),
    (r'^attribute/update/(?P<oid>[^/]+)/$', 'attribute.update'),
    (r'^attribute/update/post/(?P<oid>[^/]+)/$', 'attribute.update_post'),
    (r'^attribute/delete/(?P<oid>[^/]+)/$', 'attribute.delete'),
    (r'^attribute/display/(?P<oid>[^/]+)/$', 'attribute.display'),
    (r'^attribute/notes/(?P<oid>[^/]+)/$', 'attribute.edit_notes'),
    (r'^attribute/notes/post/(?P<oid>[^/]+)/$', 'attribute.edit_notes_post'),

    (r'^template/apply/select/(?P<target_oid>[^/]+)/(?P<template_type>[^/]+)/$', 'template.apply_select'),
    (r'^template/apply/set/(?P<target_oid>[^/]+)/(?P<template_type>[^/]+)/$', 'template.apply_set'),
    (r'^template/apply/post/(?P<target_oid>[^/]+)/(?P<template_oid>[^/]+)/$', 'template.apply_post'),

    (r'^template/(?P<template_type>[^/]+)/add/(?P<parent_oid>[^/]+)/$', 'template.add'),
    (r'^template/(?P<template_type>[^/]+)/add/post/(?P<parent_oid>[^/]+)/$', 'template.add_post'),
    (r'^template/update/(?P<oid>[^/]+)/$', 'template.update'),
    (r'^template/update/post/(?P<oid>[^/]+)/$', 'template.update_post'),
    (r'^template/delete/(?P<oid>[^/]+)/$', 'template.delete'),
    (r'^template/delete/post/(?P<oid>[^/]+)/$', 'template.delete_post'),
    (r'^template/rule/(?P<rule_type>[^/]+)/add/(?P<parent_oid>[^/]+)/$', 'template.rule_add'),
    (r'^template/rule/(?P<rule_type>[^/]+)/add/post/(?P<parent_oid>[^/]+)/$', 'template.rule_add_post'),
    (r'^template/rule/delete/(?P<oid>[^/]+)/$', 'template.rule_delete'),
    (r'^template/rule/delete/post/(?P<oid>[^/]+)/$', 'template.rule_delete_post'),
    (r'^template/display/(?P<oid>[^/]+)/$', 'template.display'),
    (r'^template/copy/(?P<oid>[^/]+)/$', 'template.copy'),
    (r'^template/copy/post/(?P<oid>[^/]+)/$', 'template.copy_post'),

    (r'^counter/(?P<parent_oid>[^/]+)/$', 'counter.index'),
    (r'^counter/basic/add/(?P<parent_oid>[^/]+)/$', 'counter.add_basic'),
    (r'^counter/basic/add/post/(?P<parent_oid>[^/]+)/$', 'counter.add_basic_post'),
    (r'^counter/looping/add/(?P<parent_oid>[^/]+)/$', 'counter.add_looping'),
    (r'^counter/looping/add/post/(?P<parent_oid>[^/]+)/$', 'counter.add_looping_post'),
    (r'^counter/update/(?P<oid>[^/]+)/$', 'counter.update'),
    (r'^counter/update/post/(?P<oid>[^/]+)/$', 'counter.update_post'),
    (r'^counter/delete/(?P<oid>[^/]+)/$', 'counter.delete'),
    (r'^counter/delete/post/(?P<oid>[^/]+)/$', 'counter.delete_post'),
    (r'^counter/display/(?P<oid>[^/]+)/$', 'counter.display'),

    (r'^networktree/(?P<parent_oid>[^/]+)/$', 'network.tree.index'),
    (r'^networktree/add/(?P<parent_oid>[^/]+)/$', 'network.tree.add'),
    (r'^networktree/add/post/(?P<parent_oid>[^/]+)/$', 'network.tree.add_post'),
    (r'^networktree/delete/(?P<oid>[^/]+)/$', 'network.tree.delete'),
    (r'^networktree/delete/post/(?P<oid>[^/]+)/$', 'network.tree.delete_post'),

    (r'^network/add/(?P<parent_oid>[^/]+)/$', 'network.add'),
    (r'^network/add/post/(?P<parent_oid>[^/]+)/$', 'network.add_post'),
    (r'^network/delete/(?P<oid>[^/]+)/$', 'network.delete'),
    (r'^network/delete/post/(?P<oid>[^/]+)/$', 'network.delete_post'),
    (r'^network/display/(?P<oid>[^/]+)/$', 'network.display'),

    (r'^network/range/add/(?P<parent_oid>[^/]+)/$', 'network.range.add'),
    (r'^network/range/add/post/(?P<parent_oid>[^/]+)/$', 'network.range.add_post'),
    (r'^network/range/delete/(?P<oid>[^/]+)/$', 'network.range.delete'),
    (r'^network/range/delete/post/(?P<oid>[^/]+)/$', 'network.range.delete_post'),
    (r'^network/range/display/(?P<oid>[^/]+)/$', 'network.range.display'),

    (r'^device/(?P<view_oid>[^/]+)/$', 'device.index'),
    (r'^device/add/template/select/(?P<parent_oid>[^/]+)/$', 'device.add_template_select'),
    (r'^device/add/template/set/(?P<parent_oid>[^/]+)/$', 'device.add_template_set'),
    (r'^device/add/template/post/(?P<parent_oid>[^/]+)/(?P<template_oid>[^/]+)/$', 'device.add_template_post'),
    (r'^device/delete/(?P<oid>[^/]+)/$', 'device.delete'),
    (r'^device/delete/post/(?P<oid>[^/]+)/$', 'device.delete_post'),
    (r'^device/disable/(?P<oid>[^/]+)/$', 'device.disable'),
    (r'^device/disable/post/(?P<oid>[^/]+)/$', 'device.disable_post'),
    (r'^device/enable/(?P<oid>[^/]+)/$', 'device.enable'),
    (r'^device/enable/post/(?P<oid>[^/]+)/$', 'device.enable_post'),
    (r'^device/display/(?P<oid>[^/]+)/$', 'device.display'),
    (r'^device/export/(?P<oid>[^/]+)/$', 'device.export'),
    (r'^device/recreate/template/select/(?P<oid>[^/]+)/$', 'device.recreate_template_select'),
    (r'^device/recreate/template/set/(?P<oid>[^/]+)/$', 'device.recreate_template_set'),
    (r'^device/recreate/template/post/(?P<oid>[^/]+)/(?P<template_oid>[^/]+)/$', 'device.recreate_template_post'),
    (r'^device/copy/(?P<oid>[^/]+)/$', 'device.copy'),
    (r'^device/copy/post/(?P<oid>[^/]+)/$', 'device.copy_post'),

    (r'^device/category/add/(?P<parent_oid>[^/]+)/$', 'device.category.add'),
    (r'^device/category/add/post/(?P<parent_oid>[^/]+)/$', 'device.category.add_post'),
    (r'^device/category/delete/(?P<oid>[^/]+)/$', 'device.category.delete'),
    (r'^device/category/delete/post/(?P<oid>[^/]+)/$', 'device.category.delete_post'),
    (r'^device/category/export/(?P<oid>[^/]+)/$', 'device.category.export'),

    (r'^device/network/add/(?P<oid>[^/]+)/$', 'device.network.add'),
    (r'^device/network/add/post/(?P<oid>[^/]+)/$', 'device.network.add_post'),
    (r'^device/network/autoassign/(?P<oid>[^/]+)/$', 'device.network.autoassign'),
    (r'^device/network/autoassign/post/(?P<oid>[^/]+)/$', 'device.network.autoassign_post'),
    (r'^device/network/delete/(?P<device_oid>[^/]+)/(?P<network_oid>[^/]+)/$', 'device.network.delete'),
    (r'^device/network/delete/post/(?P<device_oid>[^/]+)/(?P<network_oid>[^/]+)/$', 'device.network.delete_post'),

    (r'^device/(?P<type>association|reference)/delete/(?P<oid1>[^/]+)/(?P<oid2>[^/]+)/$', 'device.device_association.delete'),
    (r'^device/(?P<type>association|reference)/delete/post/(?P<oid1>[^/]+)/(?P<oid2>[^/]+)/$', 'device.device_association.delete_post'),
    (r'^device/association/add/(?P<oid>[^/]+)/$', 'device.device_association.add_with_target'),

    (r'^password/(?P<view_oid>[^/]+)/$', 'password.index'),
    (r'^password/category/add/(?P<parent_oid>[^/]+)/$', 'password.category_add'),
    (r'^password/category/add/post/(?P<parent_oid>[^/]+)/$', 'password.category_add_post'),
    (r'^password/category/delete/(?P<oid>[^/]+)/$', 'password.category_delete'),
    (r'^password/category/delete/post/(?P<oid>[^/]+)/$', 'password.category_delete_post'),
    (r'^password/category/display/(?P<oid>[^/]+)/$', 'password.category_display'),
    (r'^password/key/add/(?P<parent_oid>[^/]+)/$', 'password.key_add'),
    (r'^password/key/add/post/(?P<parent_oid>[^/]+)/$', 'password.key_add_post'),
    (r'^password/key/delete/(?P<oid>[^/]+)/$', 'password.key_delete'),
    (r'^password/key/delete/post/(?P<oid>[^/]+)/$', 'password.key_delete_post'),
    (r'^password/key/display/(?P<oid>[^/]+)/$', 'password.key_display'),
    (r'^password/add/(?P<parent_oid>[^/]+)/$', 'password.add'),
    (r'^password/add/post/(?P<parent_oid>[^/]+)/$', 'password.add_post'),
    (r'^password/delete/(?P<oid>[^/]+)/$', 'password.delete'),
    (r'^password/delete/post/(?P<oid>[^/]+)/$', 'password.delete_post'),
    (r'^password/update/(?P<oid>[^/]+)/$', 'password.update'),
    (r'^password/update/post/(?P<oid>[^/]+)/$', 'password.update_post'),

    (r'^user/$', 'user.index'),
    (r'^user/manager/display/(?P<oid>[^/]+)/$', 'user.manager_display'),
    (r'^user/manager/add/(?P<um_type>[^/]+)/$', 'user.manager_add'),
    (r'^user/manager/add/post/(?P<um_type>[^/]+)/$', 'user.manager_add_post'),
    (r'^user/manager/update/(?P<oid>[^/]+)/$', 'user.manager_update'),
    (r'^user/manager/update/post/(?P<oid>[^/]+)/$', 'user.manager_update_post'),
    (r'^user/manager/syncusers/ldap/(?P<oid>[^/]+)/$', 'user.manager_ldap_syncusers'),
    (r'^user/manager/syncusers/ldap/post/(?P<oid>[^/]+)/$', 'user.manager_ldap_syncusers_post'),
    (r'^user/manager/syncusers/ad/(?P<oid>[^/]+)/$', 'user.manager_ad_syncusers'),
    (r'^user/manager/syncusers/ad/post/(?P<oid>[^/]+)/$', 'user.manager_ad_syncusers_post'),
    (r'^user/manager/activate/(?P<oid>[^/]+)/$', 'user.manager_activate'),
    (r'^user/manager/activate/post/(?P<oid>[^/]+)/$', 'user.manager_activate_post'),
    (r'^user/manager/delete/(?P<oid>[^/]+)/$', 'user.manager_delete'),
    (r'^user/manager/delete/post/(?P<oid>[^/]+)/$', 'user.manager_delete_post'),
    (r'^user/add/(?P<oid>[^/]+)/$', 'user.add'),
    (r'^user/add/post/(?P<oid>[^/]+)/$', 'user.add_post'),
    (r'^user/display/(?P<oid>[^/]+)/$', 'user.display'),
    (r'^user/delete/(?P<oid>[^/]+)/$', 'user.delete'),
    (r'^user/delete/post/(?P<oid>[^/]+)/$', 'user.delete_post'),
    (r'^user/password/reset/(?P<oid>[^/]+)/$', 'user.reset_password'),
    (r'^user/password/reset/post/(?P<oid>[^/]+)/$', 'user.reset_password_post'),
    (r'^user/password/update/(?P<oid>[^/]+)/$', 'user.update_password'),
    (r'^user/password/update/post/(?P<oid>[^/]+)/$', 'user.update_password_post'),
    (r'^user/update/(?P<oid>[^/]+)/$', 'user.update'),
    (r'^user/update/post/(?P<oid>[^/]+)/$', 'user.update_post'),
    (r'^user/connectkey/selectkey/(?P<oid>[^/]+)/$', 'user.connectkey_selectkey'),
    (r'^user/connectkey/post/(?P<oid>[^/]+)/$', 'user.connectkey_post'),
    (r'^user/subkey/delete/(?P<oid>[^/]+)/$', 'user.subkey_delete'),
    (r'^user/subkey/delete/post/(?P<oid>[^/]+)/$', 'user.subkey_delete_post'),
    (r'^user/session/kill/(?P<session_id>[^/]+)/$', 'user.session_kill'),
    (r'^user/session/kill/post/(?P<session_id>[^/]+)/$', 'user.session_kill_post'),
    (r'^user/group/display/(?P<oid>[^/]+)/$', 'user.group_display'),
    (r'^user/group/add/(?P<oid>[^/]+)/$', 'user.group_add'),
    (r'^user/group/add/post/(?P<oid>[^/]+)/$', 'user.group_add_post'),
    (r'^user/group/update/(?P<oid>[^/]+)/$', 'user.group_update'),
    (r'^user/group/update/post/(?P<oid>[^/]+)/$', 'user.group_update_post'),
    (r'^user/group/delete/(?P<oid>[^/]+)/$', 'user.group_delete'),
    (r'^user/group/delete/post/(?P<oid>[^/]+)/$', 'user.group_delete_post'),

    (r'^config/add/select/(?P<parent_oid>[^/]+)/$', 'config.add_select'),
    (r'^config/add/set/(?P<parent_oid>[^/]+)/$', 'config.add_set'),
    (r'^config/add/post/(?P<parent_oid>[^/]+)/$', 'config.add_post'),
    (r'^config/delete/(?P<oid>[^/]+)/$', 'config.delete'),
    (r'^config/delete/post/(?P<oid>[^/]+)/$', 'config.delete_post'),

    (r'^permission/add/(?P<parent_oid>[^/]+)/$', 'permission.add'),
    (r'^permission/add/post/(?P<parent_oid>[^/]+)/$', 'permission.add_post'),
    (r'^permission/delete/(?P<oid>[^/]+)/$', 'permission.delete'),
    (r'^permission/delete/post/(?P<oid>[^/]+)/$', 'permission.delete_post'),

    (r'^command/display/(?P<oid>[^/]+)/$', 'command.display'),
    (r'^command/add/(?P<parent_oid>[^/]+)/$', 'command.add'),
    (r'^command/add/post/(?P<parent_oid>[^/]+)/$', 'command.add_post'),
    (r'^command/update/(?P<oid>[^/]+)/$', 'command.update'),
    (r'^command/update/post/(?P<oid>[^/]+)/$', 'command.update_post'),
    (r'^command/delete/(?P<oid>[^/]+)/$', 'command.delete'),
    (r'^command/delete/post/(?P<oid>[^/]+)/$', 'command.delete_post'),

    (r'^command/queue/display/(?P<oid>[^/]+)/$', 'command.queue.display'),
    (r'^command/queue/add/(?P<parent_oid>[^/]+)/$', 'command.queue.add'),
    (r'^command/queue/add/post/(?P<parent_oid>[^/]+)/$', 'command.queue.add_post'),
    (r'^command/queue/update/(?P<oid>[^/]+)/$', 'command.queue.update'),
    (r'^command/queue/update/post/(?P<oid>[^/]+)/$', 'command.queue.update_post'),
    (r'^command/queue/delete/(?P<oid>[^/]+)/$', 'command.queue.delete'),
    (r'^command/queue/delete/post/(?P<oid>[^/]+)/$', 'command.queue.delete_post'),

    (r'^event/trigger/display/(?P<oid>[^/]+)/$', 'event.trigger.display'),
    (r'^event/trigger/add/(?P<parent_oid>[^/]+)/$', 'event.trigger.add'),
    (r'^event/trigger/add/post/(?P<parent_oid>[^/]+)/$', 'event.trigger.add_post'),
    (r'^event/trigger/update/(?P<oid>[^/]+)/$', 'event.trigger.update'),
    (r'^event/trigger/update/post/(?P<oid>[^/]+)/$', 'event.trigger.update_post'),
    (r'^event/trigger/delete/(?P<oid>[^/]+)/$', 'event.trigger.delete'),
    (r'^event/trigger/delete/post/(?P<oid>[^/]+)/$', 'event.trigger.delete_post'),

    (r'^event/trigger/rule/python/display/(?P<oid>[^/]+)/$', 'event.trigger_rule_python.display'),
    (r'^event/trigger/rule/python/add/(?P<parent_oid>[^/]+)/$', 'event.trigger_rule_python.add'),
    (r'^event/trigger/rule/python/add/post/(?P<parent_oid>[^/]+)/$', 'event.trigger_rule_python.add_post'),
    (r'^event/trigger/rule/python/update/(?P<oid>[^/]+)/$', 'event.trigger_rule_python.update'),
    (r'^event/trigger/rule/python/update/post/(?P<oid>[^/]+)/$', 'event.trigger_rule_python.update_post'),
    (r'^event/trigger/rule/python/delete/(?P<oid>[^/]+)/$', 'event.trigger_rule_python.delete'),
    (r'^event/trigger/rule/python/delete/post/(?P<oid>[^/]+)/$', 'event.trigger_rule_python.delete_post'),

    (r'^tag/(?P<oid>[^/]+)/$', 'root.tag_oid'),
    (r'^untag/(?P<oid>[^/]+)/$', 'root.untag_oid'),
    (r'^relocate/tagged/(?P<oid>[^/]+)/$', 'root.relocate_tagged_oid'),
    (r'^toggle-verbose/(?P<oid>.*)/$', 'root.toggle_verbose'),
    (r'^search/$', 'root.search'),
    (r'^login/$', 'root.login'),
    (r'^logout/$', 'root.logout'),
    (r'^dinfo/$', 'root.dinfo'),
    (r'^style.css$', 'root.style'),
    (r'^prototype.js$', 'root.prototypejs'),
)

