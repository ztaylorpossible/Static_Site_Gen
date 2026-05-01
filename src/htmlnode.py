class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        attributes = ""
        if self.props == None or len(self.props) == 0:
            return ""
        for key, value in self.props.items():
            attributes += f'{key}="{value}" '
        attributes = attributes[:-1]
        return attributes

    def __repr__(self):
        children = len(self.children) if self.children else 0
        return f"HTMLNode: tag={self.tag} value={self.value} children={children} props={self.props_to_html()}"
