# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import pymel.core as pm


def selected():
    return pm.ls(sl=True)[0]


def plugin_loaded(plugin):
    return mc.pluginInfo(plugin, q=1, loaded=1)


def load_plugin(plugin):
    if not plugin_loaded(plugin):
        mc.loadPlugin(plugin, quiet=1)
    return True


def open_file(file_name, lnr=False):
    mc.file(file_name, open=1, f=1, loadNoReferences=lnr)


def selected():
    return mc.ls(sl=1)


def export_selected(file_path, pr_flag=False):
    """
    :param file_path:a maya file path
    :param pr_flag: if True: export still as reference, else: import
    :return:
    """
    sel = mc.ls(sl=1)
    if not sel:
        print "[LIBER] info: Nothing selected."
        return
    parent_dir = os.path.dirname(file_path)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
    maya_type = get_file_type(file_path)
    mc.file(file_path, typ=maya_type, options="v=0", force=1, es=1, pr=pr_flag)


def export_obj(start, end, path, padding=4):
    parent_dir = os.path.dirname(path)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
    for i in range(start, end+1):
        mc.currentTime(i)
        prefix, suffix = os.path.splitext(path)
        new_path = "%s.%s%s" % (prefix, str(i).zfill(padding), suffix)
        mc.file(new_path, typ="OBJexport", options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", pr=1, es=1)


def get_file_type(path):
    file_type = None
    if path.endswith(".abc"):
        file_type = "Alembic"
    elif path.endswith(".mb"):
        file_type = "mayaBinary"
    elif path.endswith(".ma"):
        file_type = "mayaAscii"
    elif path.endswith(".fbx"):
        file_type = "Fbx"
    elif path.endswith(".obj"):
        file_type = "OBJexport"
    return file_type


def maya_import(file_path):
    file_type = get_file_type(file_path)
    mc.file(file_path, i=1, type=file_type, ignoreVersion=1, ra=1,
            mergeNamespacesOnClash=0, namespace=":", options="v=0", pr=1)


def export_abc(start_frame, end_frame, tar_path, root, uv_write=True, renderable_only=True, attribute=None):
    if isinstance(root, basestring):
        root = [root]
    if isinstance(attribute, basestring):
        attribute = [attribute]
    tar_dir = os.path.dirname(tar_path)
    if not os.path.isdir(tar_dir):
        os.makedirs(tar_dir)
    load_plugin("AbcExport.mll")
    j_base_string = "-frameRange {start_frame} {end_frame} -worldSpace" \
                    " -writeVisibility -file {tar_path}"
    if uv_write:
        j_base_string += " -uvWrite"
    if renderable_only:
        j_base_string += " -renderableOnly"
    if attribute:
        for attr in attribute:
            j_base_string += " -u %s" % attr
    for r in root:
        j_base_string += " -root %s" % r
    j_string = j_base_string.format(start_frame=start_frame, end_frame=end_frame, tar_path=tar_path)
    mc.AbcExport(j=j_string)


def import_abc(abc_path):
    mc.AbcImport(abc_path)


def create_reference(path, namespace_name=":", allow_repeat=False, get_group=False):
    result = None
    path = path.replace("\\", "/")
    if path.endswith(".abc"):
        load_plugin("AbcImport.mll")
    file_type = get_file_type(path)
    if allow_repeat:
        result = pm.system.createReference(path, loadReferenceDepth="all",
                                           mergeNamespacesOnClash=False,
                                           namespace=namespace_name,
                                           type=file_type)
    else:
        references = pm.listReferences()
        if not references:
            print "*" * 100
            result = pm.system.createReference(path, loadReferenceDepth="all",
                                               ignoreVersion=1, gl=1,
                                               options="v=0",
                                               mergeNamespacesOnClash=True,
                                               namespace=namespace_name,
                                               type=file_type)
        else:
            reference_paths = [ref.path for ref in references]
            if path not in reference_paths:
                result = pm.system.createReference(path, loadReferenceDepth="all",
                                                   mergeNamespacesOnClash=True,
                                                   namespace=namespace_name,
                                                   type=file_type)
            else:
                ref_node = pm.referenceQuery(path, referenceNode=1)
                if not pm.referenceQuery(ref_node, isLoaded=1):
                    pm.system.loadReference(path)
    if get_group:
        return pm.referenceQuery(result.refNode, dagPath=1, nodes=1)[0]


def export_rs(file_name, start, end):
    dir_name = os.path.dirname(file_name)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    mc.file(file_name, pr=1, es=1, force=1, typ="Redshift Proxy",
            options="startFrame=%s;endFrame=%s;frameStep=1;exportConnectivity=0;" % (start, end))


def import_rs(file_name):
    rs_proxy_node = mc.createNode("RedshiftProxyMesh", name="redshiftProxy")
    rs_proxy_placeholder_shape = mc.createNode("mesh", name="temp")
    transform = mc.listRelatives(rs_proxy_placeholder_shape, parent=1)[0]
    transform = mc.rename(transform, "redshiftProxyPlaceholder")
    rs_proxy_placeholder_shape = mc.rename(rs_proxy_placeholder_shape, "%sShape" % transform)
    mc.connectAttr("%s.outMesh" % rs_proxy_node, "%s.inMesh" % rs_proxy_placeholder_shape, f=1)
    mc.setAttr("%s.fn" % rs_proxy_node, file_name, type="string")
    return rs_proxy_node


if __name__ == "__main__":
    pass
