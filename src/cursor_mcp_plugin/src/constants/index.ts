// Plugin Constants
export const DEFAULT_SERVER_PORT = 3055;

export const PLUGIN_DIMENSIONS = {
  width: 350,
  height: 450
};

export const COMMANDS = {
  // Document commands
  GET_DOCUMENT_INFO: 'get_document_info',
  GET_SELECTION: 'get_selection',
  GET_NODE_INFO: 'get_node_info',
  GET_NODES_INFO: 'get_nodes_info',
  GET_NODE_CHILDREN: 'get_node_children',
  READ_MY_DESIGN: 'read_my_design',
  
  // Create commands
  CREATE_RECTANGLE: 'create_rectangle',
  CREATE_FRAME: 'create_frame',
  CREATE_TEXT: 'create_text',
  
  // Style commands
  SET_FILL_COLOR: 'set_fill_color',
  SET_STROKE_COLOR: 'set_stroke_color',
  SET_CORNER_RADIUS: 'set_corner_radius',
  
  // Transform commands
  MOVE_NODE: 'move_node',
  RESIZE_NODE: 'resize_node',
  CLONE_NODE: 'clone_node',
  
  // Delete commands
  DELETE_NODE: 'delete_node',
  DELETE_MULTIPLE_NODES: 'delete_multiple_nodes',
  
  // Text commands
  SET_TEXT_CONTENT: 'set_text_content',
  SCAN_TEXT_NODES: 'scan_text_nodes',
  SET_MULTIPLE_TEXT_CONTENTS: 'set_multiple_text_contents',
  
  // Component commands
  GET_STYLES: 'get_styles',
  GET_LOCAL_COMPONENTS: 'get_local_components',
  CREATE_COMPONENT_INSTANCE: 'create_component_instance',
  GET_INSTANCE_OVERRIDES: 'get_instance_overrides',
  SET_INSTANCE_OVERRIDES: 'set_instance_overrides',
  
  // Layout commands
  SET_LAYOUT_MODE: 'set_layout_mode',
  SET_PADDING: 'set_padding',
  SET_AXIS_ALIGN: 'set_axis_align',
  SET_LAYOUT_SIZING: 'set_layout_sizing',
  SET_ITEM_SPACING: 'set_item_spacing',
  
  // Export commands
  EXPORT_NODE_AS_IMAGE: 'export_node_as_image',
  
  // Annotation commands
  GET_ANNOTATIONS: 'get_annotations',
  SET_ANNOTATION: 'set_annotation',
  SCAN_NODES_BY_TYPES: 'scan_nodes_by_types',
  SET_MULTIPLE_ANNOTATIONS: 'set_multiple_annotations',
  
  // Reaction commands
  GET_REACTIONS: 'get_reactions',
  
  // Connection commands
  SET_DEFAULT_CONNECTOR: 'set_default_connector',
  CREATE_CONNECTIONS: 'create_connections'
};

export const MESSAGE_TYPES = {
  UPDATE_SETTINGS: 'update-settings',
  NOTIFY: 'notify',
  CLOSE_PLUGIN: 'close-plugin',
  EXECUTE_COMMAND: 'execute-command',
  COMMAND_RESULT: 'command-result',
  COMMAND_ERROR: 'command-error',
  AUTO_CONNECT: 'auto-connect',
  INIT_SETTINGS: 'init-settings',
  COMMAND_PROGRESS: 'command_progress'
};

export const PROGRESS_STATUS = {
  STARTED: 'started',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  ERROR: 'error'
};