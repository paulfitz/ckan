from ckan import model
from ckan.common import json
from ckan.lib import uploader

class HappyDumper(object):
    '''Dumps package data, adding paths to local resources when applicable'''
    def dump(self, dump_file_obj):
        query = model.Session.query(model.Package)
        query = query.filter_by(state=model.State.ACTIVE)
        pkgs = []
        for pkg in query:
            pkg_dict = pkg.as_dict()
            for res in pkg_dict['resources']:
                if res['url_type'] == 'upload':
                    upload = uploader.ResourceUpload(res)
                    res['path'] = upload.get_path(res['id'])
            pkgs.append(pkg_dict)
        json.dump(pkgs, dump_file_obj, indent=4)
