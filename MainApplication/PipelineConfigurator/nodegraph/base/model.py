
import json
from collections import defaultdict

from ..constants import (
    NODE_PROP,
    NODE_PROP_QLABEL,
    NODE_PROP_QLINEEDIT,
    NODE_PROP_QCHECKBOX,
    NODE_PROP_COLORPICKER
)

from ..errors import NodePropertyError


class PortModel(object):
    """
    Data dump for a port object.
    """

    def __init__(self, node):
        self.node = node
        self.type_ = ''
        self.name = 'port'
        self.display_name = True
        self.multi_connection = False
        self.visible = True
        self.locked = False
        self.connected_ports = defaultdict(list)

        # GAPA Data
        self.data_type = None
        self.uid = None

    def __repr__(self):
        return '<{}(\'{}\') object at {}>'.format(
            self.__class__.__name__, self.name, hex(id(self)))

    @property
    def to_dict(self):
        """
        serialize model information to a dictionary.

        Returns:
            dict: node port dictionary eg.
                {
                    'type': 'in',
                    'name': 'port',
                    'display_name': True,
                    'multi_connection': False,
                    'visible': True,
                    'locked': False,
                    'connected_ports': {<node_id>: [<port_name>, <port_name>]}
                }
        """
        props = self.__dict__.copy()
        props.pop('node')
        props['connected_ports'] = dict(props.pop('connected_ports'))
        return props


class NodeModel(object):
    """
    Data dump for a node object.
    """

    def __init__(self):
        self.type_ = None
        self.id = hex(id(self))
        self.icon = None
        self.name = 'node'
        self.color = (13, 18, 23, 255)
        self.border_color = (74, 84, 85, 255)
        self.text_color = (255, 255, 255, 180)
        self.disabled = False
        self.selected = False
        self.visible = True
        self.width = 100.0
        self.height = 80.0
        self.pos = [0.0, 0.0]

        # GAPA Data
        self.uid = None
        self.program = ""
        self.is_plugin = False
        self.has_set_outputs = False
        self.export_all = False
        self.settings = {}
        self.config = None

        # BaseNode attrs.
        self.input_ports = {}
        self.output_ports = {}
        self.info = None
        self.port_deletion_allowed = False

        # GroupNode attrs.
        self.subgraph_session = {}

        # Custom
        self._custom_properties = {}

        # node graph model set at node added time.
        self._graph_model = None

        # store the property attributes.
        # (deleted when node is added to the graph)
        self._TEMP_property_attrs = {}

        # temp store the property widget types.
        # (deleted when node is added to the graph)
        self._TEMP_property_widget_types = {
            'type_': NODE_PROP_QLABEL,
            'id': NODE_PROP_QLABEL,
            'icon': NODE_PROP,
            'name': NODE_PROP_QLINEEDIT,
            'color': NODE_PROP_COLORPICKER,
            'border_color': NODE_PROP,
            'text_color': NODE_PROP_COLORPICKER,
            'disabled': NODE_PROP_QCHECKBOX,
            'selected': NODE_PROP,
            'width': NODE_PROP,
            'height': NODE_PROP,
            'pos': NODE_PROP,
            'inputs': NODE_PROP,
            'outputs': NODE_PROP,
            'info': NODE_PROP,
        }

    def __repr__(self):
        return '<{}(\'{}\') object at {}>'.format(
            self.__class__.__name__, self.name, self.id)

    def add_property(self, name, value, items=None, range=None,
                     widget_type=NODE_PROP, tab=None):
        """
        add custom property.

        Args:
            name (str): name of the property.
            value (object): data.
            items (list[str]): items used by widget type NODE_PROP_QCOMBO.
            range (tuple)): min, max values used by NODE_PROP_SLIDER.
            widget_type (int): widget type flag.
            tab (str): widget tab name.
        """
        tab = tab or 'Properties'

        if name in self.properties.keys():
            raise NodePropertyError(
                '"{}" reserved for default property.'.format(name))
        if name in self._custom_properties.keys():
            raise NodePropertyError(
                '"{}" property already exists.'.format(name))

        self._custom_properties[name] = value

        if self._graph_model is None:
            self._TEMP_property_widget_types[name] = widget_type
            self._TEMP_property_attrs[name] = {'tab': tab}
            if items:
                self._TEMP_property_attrs[name]['items'] = items
            if range:
                self._TEMP_property_attrs[name]['range'] = range
        else:
            attrs = {self.type_: {name: {
                'widget_type': widget_type,
                'tab': tab
            }}}
            if items:
                attrs[self.type_][name]['items'] = items
            if range:
                attrs[self.type_][name]['range'] = range
            self._graph_model.set_node_common_properties(attrs)

    def set_property(self, name, value):
        if name in self.properties.keys():
            setattr(self, name, value)
        elif name in self._custom_properties.keys():
            self._custom_properties[name] = value
        else:
            raise NodePropertyError('No property "{}"'.format(name))

    def get_property(self, name):
        if name in self.properties.keys():
            return self.properties[name]
        return self._custom_properties.get(name)

    def get_widget_type(self, name):
        model = self._graph_model
        if model is None:
            return self._TEMP_property_widget_types.get(name)
        return model.get_node_common_properties(self.type_)[name]['widget_type']

    def get_tab_name(self, name):
        model = self._graph_model
        if model is None:
            attrs = self._TEMP_property_attrs.get(name)
            if attrs:
                return attrs[name].get('tab')
            return
        return model.get_node_common_properties(self.type_)[name]['tab']

    @property
    def properties(self):
        """
        return all default node properties.

        Returns:
            dict: default node properties.
        """
        props = self.__dict__.copy()
        exclude = ['_custom_properties',
                   '_graph_model',
                   '_TEMP_property_attrs',
                   '_TEMP_property_widget_types']
        [props.pop(i) for i in exclude if i in props.keys()]
        return props

    @property
    def custom_properties(self):
        """
        return all custom properties specified by the user.

        Returns:
            dict: user defined properties.
        """
        return self._custom_properties

    @property
    def to_dict(self):
        """
        serialize model information to a dictionary.

        Returns:
            dict: node id as the key and properties as the values eg.
                {'0x106cf75a8': {
                    'name': 'foo node',
                    'color': (48, 58, 69, 255),
                    'border_color': (85, 100, 100, 255),
                    'text_color': (255, 255, 255, 180),
                    'type_': 'com.chantasticvfx.FooNode',
                    'selected': False,
                    'disabled': False,
                    'visible': True,
                    'width': 0.0,
                    'height: 0.0,
                    'pos': (0.0, 0.0),
                    'custom': {},
                    'inputs': {
                        <port_name>: {<node_id>: [<port_name>, <port_name>]}
                    },
                    'outputs': {
                        <port_name>: {<node_id>: [<port_name>, <port_name>]}
                    },
                    'input_ports': [<port_name>, <port_name>],
                    'output_ports': [<port_name>, <port_name>],
                    },
                    subgraph_session: <sub graph session data>
                }
        """
        node_dict = self.__dict__.copy()
        node_id = node_dict.pop('id')

        inputs = {}
        outputs = {}
        input_ports = []
        output_ports = []
        for name, model in node_dict.pop('input_ports').items():
            if self.port_deletion_allowed:
                input_ports.append({
                    'name': name,
                    'multi_connection': model.multi_connection,
                    'display_name': model.display_name,
                    'uid': model.uid,
                    'data_type': model.data_type,
                })
            connected_ports = model.to_dict['connected_ports']
            if connected_ports:
                inputs[name] = connected_ports
        for name, model in node_dict.pop('output_ports').items():
            if self.port_deletion_allowed:
                output_ports.append({
                    'name': name,
                    'multi_connection': model.multi_connection,
                    'display_name': model.display_name,
                    'uid': model.uid,
                    'data_type': model.data_type,
                })
            connected_ports = model.to_dict['connected_ports']
            if connected_ports:
                outputs[name] = connected_ports
        if inputs:
            node_dict['input'] = inputs
        if outputs:
            node_dict['outputs'] = outputs

        if self.port_deletion_allowed:
            node_dict['input_ports'] = input_ports
            node_dict['output_ports'] = output_ports

        if self.subgraph_session:
            node_dict['subgraph_session'] = self.subgraph_session

        custom_props = node_dict.pop('_custom_properties', {})
        if custom_props:
            node_dict['custom'] = custom_props

        exclude = ['_graph_model',
                   '_TEMP_property_attrs',
                   '_TEMP_property_widget_types']
        [node_dict.pop(i) for i in exclude if i in node_dict.keys()]

        return {node_id: node_dict}

    @property
    def serial(self):
        """
        Serialize model information to a string.

        Returns:
            str: serialized JSON string.
        """
        model_dict = self.to_dict
        return json.dumps(model_dict)


class NodeGraphModel(object):
    """
    Data dump for a node graph.
    """

    def __init__(self):
        self.__common_node_properties = {}

        self.nodes = {}
        self.session = ''
        self.acyclic = True
        self.pipe_collision = False

    def common_properties(self):
        """
        Return all common node properties.

        Returns:
            dict: common node properties.
                eg.
                    {'nodegraph.nodes.FooNode': {
                        'my_property': {
                            'widget_type': 0,
                            'tab': 'Properties',
                            'items': ['foo', 'bar', 'test'],
                            'range': (0, 100)
                            }
                        }
                    }
        """
        return self.__common_node_properties

    def set_node_common_properties(self, attrs):
        """
        Store common node properties.

        Args:
            attrs (dict): common node properties.
                eg.
                    {'nodegraph.nodes.FooNode': {
                        'my_property': {
                            'widget_type': 0,
                            'tab': 'Properties',
                            'items': ['foo', 'bar', 'test'],
                            'range': (0, 100)
                            }
                        }
                    }
        """
        for node_type in attrs.keys():
            node_props = attrs[node_type]

            if node_type not in self.__common_node_properties.keys():
                self.__common_node_properties[node_type] = node_props
                continue

            for prop_name, prop_attrs in node_props.items():
                common_props = self.__common_node_properties[node_type]
                if prop_name not in common_props.keys():
                    common_props[prop_name] = prop_attrs
                    continue
                common_props[prop_name].update(prop_attrs)

    def get_node_common_properties(self, node_type):
        """
        Return all the common properties for a registered node.

        Args:
            node_type (str): node type.

        Returns:
            dict: node common properties.
        """
        return self.__common_node_properties.get(node_type)
