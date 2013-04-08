

#Creds to pymclevel
def Tag(tagName, tagType, default_or_func=None):
    def getter(self):
        if tagName not in self.tag:
            if hasattr(default_or_func, "__call__"):
                default = default_or_func(self)
            else:
                default = default_or_func

            self.tag[tagName] = tagType(default)
        return self.tag[tagName].value

    def setter(self, val):
        self.tag[tagName] = tagType(value=val)

    return property(getter, setter)
