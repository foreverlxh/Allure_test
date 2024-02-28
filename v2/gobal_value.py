class g_var(object):
    _global_dict={} #最大程度，保证这个字典不被污染

    def set_dict(self,key,value):
        self._global_dict[key] = value


    def get_dict(self,key):
        return self._global_dict[key]

    def show_dict(self):
        return self._global_dict