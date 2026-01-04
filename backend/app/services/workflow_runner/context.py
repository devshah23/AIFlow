class WfExecutionContext:
    def __init__(self):
        self.data = {}

    def to_dict(self):
        return self.data

    def set(self, key,type, value):
        if isinstance(value, str):
            self.data[key] = {"type":type,"output":value}
        else:
            value["type"]=type
            self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def get_output(self, key):
        node_data= self.data.get(key, {})
        if node_data["output"] is not None:
            return node_data["output"]
        return ''
    
    def get_output_with_node_type(self,key):
        node_data= self.data.get(key, {})
        if node_data["output"]:
            return "Type:"+node_data["type"]+"\nOutput:"+node_data["output"]
        return None
