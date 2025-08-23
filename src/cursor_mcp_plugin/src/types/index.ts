// Type definitions for the plugin

export interface PluginState {
  serverPort: number;
}

export interface CommandParams {
  [key: string]: any;
}

export interface CommandResult {
  success?: boolean;
  message?: string;
  error?: string;
  [key: string]: any;
}

export interface ProgressUpdate {
  type: 'command_progress';
  commandId: string;
  commandType: string;
  status: 'started' | 'in_progress' | 'completed' | 'error';
  progress: number;
  totalItems: number;
  processedItems: number;
  message: string;
  timestamp: number;
  currentChunk?: number;
  totalChunks?: number;
  chunkSize?: number;
  payload?: any;
}

export interface UIMessage {
  type: string;
  [key: string]: any;
}

export interface CommandMessage extends UIMessage {
  type: 'execute-command';
  id: string;
  command: string;
  params: CommandParams;
}

export interface Color {
  r: number;
  g: number;
  b: number;
  a?: number;
}

export interface NodeInfo {
  id: string;
  name: string;
  type: string;
  visible?: boolean;
  [key: string]: any;
}

export interface TextNodeInfo extends NodeInfo {
  characters: string;
  fontSize: number;
  fontFamily: string;
  fontStyle: string;
  x: number;
  y: number;
  width: number;
  height: number;
  path: string;
  depth: number;
}

export interface Annotation {
  nodeId: string;
  labelMarkdown: string;
  categoryId?: string;
  properties?: Array<{ key: string; value: string }>;
}

export interface Connection {
  startNodeId: string;
  endNodeId: string;
  text?: string;
}

export interface InstanceOverrideData {
  sourceInstanceId: string;
  targetNodeIds: string[];
}

export interface ExportNodeAsImageParams {
  nodeId: string;
  format?: string;
  scale?: number;
}

export interface ExportNodeAsImageResult {
  nodeId: string;
  format: string;
  scale: number;
  mimeType: string;
  imageData: string;
  success: boolean;
  timestamp: number;
}