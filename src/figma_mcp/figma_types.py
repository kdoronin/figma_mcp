"""Type definitions for Figma MCP Server."""

from typing import Dict, List, Optional, Any, Union, Literal
from enum import Enum
from pydantic import BaseModel
import uuid


class FigmaCommand(str, Enum):
    """Available Figma commands."""
    GET_DOCUMENT_INFO = "get_document_info"
    GET_SELECTION = "get_selection"
    GET_NODE_INFO = "get_node_info"
    GET_NODES_INFO = "get_nodes_info"
    GET_NODE_CHILDREN = "get_node_children"
    READ_MY_DESIGN = "read_my_design"
    DELETE_NODE = "delete_node"
    DELETE_MULTIPLE_NODES = "delete_multiple_nodes"
    GET_STYLES = "get_styles"
    GET_LOCAL_COMPONENTS = "get_local_components"
    GET_INSTANCE_OVERRIDES = "get_instance_overrides"
    SET_INSTANCE_OVERRIDES = "set_instance_overrides"
    EXPORT_NODE_AS_IMAGE = "export_node_as_image"
    JOIN = "join"
    SET_CORNER_RADIUS = "set_corner_radius"
    CLONE_NODE = "clone_node"
    SET_TEXT_CONTENT = "set_text_content"
    SCAN_TEXT_NODES = "scan_text_nodes"
    SET_MULTIPLE_TEXT_CONTENTS = "set_multiple_text_contents"
    GET_ANNOTATIONS = "get_annotations"
    SET_ANNOTATION = "set_annotation"
    SET_MULTIPLE_ANNOTATIONS = "set_multiple_annotations"
    SCAN_NODES_BY_TYPES = "scan_nodes_by_types"
    SET_LAYOUT_MODE = "set_layout_mode"
    SET_PADDING = "set_padding"
    SET_AXIS_ALIGN = "set_axis_align"
    SET_LAYOUT_SIZING = "set_layout_sizing"
    SET_ITEM_SPACING = "set_item_spacing"
    GET_REACTIONS = "get_reactions"
    SET_DEFAULT_CONNECTOR = "set_default_connector"
    CREATE_CONNECTIONS = "create_connections"
    MOVE_NODE = "move_node"
    RESIZE_NODE = "resize_node"
    SET_FILL_COLOR = "set_fill_color"
    SET_STROKE_COLOR = "set_stroke_color"


class Color(BaseModel):
    """RGB color with optional alpha."""
    r: float
    g: float
    b: float
    a: Optional[float] = 1.0


class FigmaResponse(BaseModel):
    """Standard Figma response structure."""
    id: str
    result: Optional[Any] = None
    error: Optional[str] = None


class CommandProgressStatus(str, Enum):
    """Command execution status."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


class CommandProgressUpdate(BaseModel):
    """Progress update for long-running commands."""
    type: Literal["command_progress"] = "command_progress"
    commandId: str
    commandType: str
    status: CommandProgressStatus
    progress: int
    totalItems: int
    processedItems: int
    currentChunk: Optional[int] = None
    totalChunks: Optional[int] = None
    chunkSize: Optional[int] = None
    message: str
    payload: Optional[Any] = None
    timestamp: int


class ComponentOverride(BaseModel):
    """Component override information."""
    id: str
    overriddenFields: List[str]


class GetInstanceOverridesResult(BaseModel):
    """Result of getting instance overrides."""
    success: bool
    message: str
    sourceInstanceId: str
    mainComponentId: str
    overridesCount: int


class InstanceOverrideResult(BaseModel):
    """Result for single instance override."""
    success: bool
    instanceId: str
    instanceName: str
    appliedCount: Optional[int] = None
    message: Optional[str] = None


class SetInstanceOverridesResult(BaseModel):
    """Result of setting instance overrides."""
    success: bool
    message: str
    totalCount: Optional[int] = None
    results: Optional[List[InstanceOverrideResult]] = None


class AnnotationProperty(BaseModel):
    """Annotation property."""
    type: str


class AnnotationParams(BaseModel):
    """Parameters for single annotation."""
    nodeId: str
    labelMarkdown: str
    categoryId: Optional[str] = None
    annotationId: Optional[str] = None
    properties: Optional[List[AnnotationProperty]] = None


class SetMultipleAnnotationsParams(BaseModel):
    """Parameters for setting multiple annotations."""
    nodeId: str
    annotations: List[AnnotationParams]


class AnnotationResult(BaseModel):
    """Result for single annotation operation."""
    success: bool
    nodeId: str
    error: Optional[str] = None
    annotationId: Optional[str] = None


class AnnotationsResult(BaseModel):
    """Result of annotation operations."""
    success: bool
    nodeId: str
    annotationsApplied: Optional[int] = None
    annotationsFailed: Optional[int] = None
    totalAnnotations: Optional[int] = None
    completedInChunks: Optional[int] = None
    results: Optional[List[AnnotationResult]] = None


class TextContentItem(BaseModel):
    """Text content for node."""
    nodeId: str
    text: str


class TextReplaceResult(BaseModel):
    """Result for single text replacement."""
    success: bool
    nodeId: str
    error: Optional[str] = None
    originalText: Optional[str] = None
    translatedText: Optional[str] = None


class TextReplacementResult(BaseModel):
    """Result of text replacement operations."""
    success: bool
    nodeId: str
    replacementsApplied: Optional[int] = None
    replacementsFailed: Optional[int] = None
    totalReplacements: Optional[int] = None
    completedInChunks: Optional[int] = None
    results: Optional[List[TextReplaceResult]] = None


class Connection(BaseModel):
    """Connection between nodes."""
    startNodeId: str
    endNodeId: str
    text: Optional[str] = None


class ExportFormat(str, Enum):
    """Export formats for nodes."""
    PNG = "PNG"
    JPG = "JPG"
    SVG = "SVG"
    PDF = "PDF"


# Command parameter types
class GetDocumentInfoParams(BaseModel):
    """Parameters for get_document_info command."""
    pass


class GetSelectionParams(BaseModel):
    """Parameters for get_selection command."""
    pass


class GetNodeInfoParams(BaseModel):
    """Parameters for get_node_info command."""
    nodeId: str


class GetNodesInfoParams(BaseModel):
    """Parameters for get_nodes_info command."""
    nodeIds: List[str]


class GetNodeChildrenParams(BaseModel):
    """Parameters for get_node_children command."""
    nodeId: str


class ReadMyDesignParams(BaseModel):
    """Parameters for read_my_design command."""
    pass


class DeleteNodeParams(BaseModel):
    """Parameters for delete_node command."""
    nodeId: str


class DeleteMultipleNodesParams(BaseModel):
    """Parameters for delete_multiple_nodes command."""
    nodeIds: List[str]


class GetStylesParams(BaseModel):
    """Parameters for get_styles command."""
    pass


class GetLocalComponentsParams(BaseModel):
    """Parameters for get_local_components command."""
    pass


class GetInstanceOverridesParams(BaseModel):
    """Parameters for get_instance_overrides command."""
    instanceNodeId: Optional[str] = None


class SetInstanceOverridesParams(BaseModel):
    """Parameters for set_instance_overrides command."""
    targetNodeIds: List[str]
    sourceInstanceId: str


class ExportNodeAsImageParams(BaseModel):
    """Parameters for export_node_as_image command."""
    nodeId: str
    format: Optional[ExportFormat] = ExportFormat.PNG
    scale: Optional[float] = 1.0


class JoinParams(BaseModel):
    """Parameters for join command."""
    channel: str


class SetCornerRadiusParams(BaseModel):
    """Parameters for set_corner_radius command."""
    nodeId: str
    radius: float
    corners: Optional[List[bool]] = None


class CloneNodeParams(BaseModel):
    """Parameters for clone_node command."""
    nodeId: str
    x: Optional[float] = None
    y: Optional[float] = None


class SetTextContentParams(BaseModel):
    """Parameters for set_text_content command."""
    nodeId: str
    text: str


class ScanTextNodesParams(BaseModel):
    """Parameters for scan_text_nodes command."""
    nodeId: str
    useChunking: bool
    chunkSize: int


class SetMultipleTextContentsParams(BaseModel):
    """Parameters for set_multiple_text_contents command."""
    nodeId: str
    text: List[TextContentItem]


class GetAnnotationsParams(BaseModel):
    """Parameters for get_annotations command."""
    nodeId: Optional[str] = None
    includeCategories: Optional[bool] = False


class SetAnnotationParams(BaseModel):
    """Parameters for set_annotation command."""
    nodeId: str
    annotationId: Optional[str] = None
    labelMarkdown: str
    categoryId: Optional[str] = None
    properties: Optional[List[AnnotationProperty]] = None


class ScanNodesByTypesParams(BaseModel):
    """Parameters for scan_nodes_by_types command."""
    nodeId: str
    types: List[str]


class SetLayoutModeParams(BaseModel):
    """Parameters for set_layout_mode command."""
    nodeId: str
    layoutMode: str


class SetPaddingParams(BaseModel):
    """Parameters for set_padding command."""
    nodeId: str
    padding: Union[float, List[float]]


class SetAxisAlignParams(BaseModel):
    """Parameters for set_axis_align command."""
    nodeId: str
    primaryAxisAlignItems: str
    counterAxisAlignItems: str


class SetLayoutSizingParams(BaseModel):
    """Parameters for set_layout_sizing command."""
    nodeId: str
    primaryAxisSizingMode: str
    counterAxisSizingMode: str


class SetItemSpacingParams(BaseModel):
    """Parameters for set_item_spacing command."""
    nodeId: str
    itemSpacing: float


class GetReactionsParams(BaseModel):
    """Parameters for get_reactions command."""
    nodeIds: List[str]


class SetDefaultConnectorParams(BaseModel):
    """Parameters for set_default_connector command."""
    connectorId: Optional[str] = None


class CreateConnectionsParams(BaseModel):
    """Parameters for create_connections command."""
    connections: List[Connection]


class MoveNodeParams(BaseModel):
    """Parameters for move_node command."""
    nodeId: str
    x: float
    y: float


class ResizeNodeParams(BaseModel):
    """Parameters for resize_node command."""
    nodeId: str
    width: float
    height: float


class SetFillColorParams(BaseModel):
    """Parameters for set_fill_color command."""
    nodeId: str
    r: float
    g: float
    b: float
    a: Optional[float] = 1.0


class SetStrokeColorParams(BaseModel):
    """Parameters for set_stroke_color command."""
    nodeId: str
    r: float
    g: float
    b: float
    a: Optional[float] = 1.0
    weight: Optional[float] = None


# Union type for all command parameters
CommandParams = Union[
    GetDocumentInfoParams,
    GetSelectionParams,
    GetNodeInfoParams,
    GetNodesInfoParams,
    ReadMyDesignParams,
    DeleteNodeParams,
    DeleteMultipleNodesParams,
    GetStylesParams,
    GetLocalComponentsParams,
    GetInstanceOverridesParams,
    SetInstanceOverridesParams,
    ExportNodeAsImageParams,
    JoinParams,
    SetCornerRadiusParams,
    CloneNodeParams,
    SetTextContentParams,
    ScanTextNodesParams,
    SetMultipleTextContentsParams,
    GetAnnotationsParams,
    SetAnnotationParams,
    SetMultipleAnnotationsParams,
    ScanNodesByTypesParams,
    SetLayoutModeParams,
    SetPaddingParams,
    SetAxisAlignParams,
    SetLayoutSizingParams,
    SetItemSpacingParams,
    GetReactionsParams,
    SetDefaultConnectorParams,
    CreateConnectionsParams,
    MoveNodeParams,
    ResizeNodeParams,
    SetFillColorParams,
    SetStrokeColorParams,
]


class PendingRequest(BaseModel):
    """Pending request information."""
    id: str
    future: Any  # asyncio.Future
    timeout_handle: Any  # asyncio.Handle
    last_activity: float


class ProgressMessage(BaseModel):
    """Progress message structure."""
    message: Union[FigmaResponse, Dict[str, Any]]
    type: Optional[str] = None
    id: Optional[str] = None

    class Config:
        extra = "allow"


class WebSocketRequest(BaseModel):
    """WebSocket request structure."""
    id: str
    type: str
    channel: Optional[str] = None
    message: Optional[Dict[str, Any]] = None


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


def rgba_to_hex(color: Any) -> str:
    """Convert RGBA color to hex string."""
    if not color:
        return "#000000"
    
    # Handle different color formats
    if isinstance(color, dict):
        r = int((color.get('r', 0) * 255))
        g = int((color.get('g', 0) * 255))
        b = int((color.get('b', 0) * 255))
    else:
        # Assume it's already in 0-255 range
        r = int(color.get('r', 0)) if hasattr(color, 'get') else 0
        g = int(color.get('g', 0)) if hasattr(color, 'get') else 0
        b = int(color.get('b', 0)) if hasattr(color, 'get') else 0
    
    return f"#{r:02x}{g:02x}{b:02x}" 