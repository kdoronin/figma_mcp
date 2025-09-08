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
    GET_STYLES = "get_styles"
    GET_LOCAL_COMPONENTS = "get_local_components"
    GET_INSTANCE_OVERRIDES = "get_instance_overrides"
    EXPORT_NODE_AS_IMAGE = "export_node_as_image"
    JOIN = "join"
    SCAN_TEXT_NODES = "scan_text_nodes"
    GET_ANNOTATIONS = "get_annotations"
    SCAN_NODES_BY_TYPES = "scan_nodes_by_types"
    GET_REACTIONS = "get_reactions"


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


class GetStylesParams(BaseModel):
    """Parameters for get_styles command."""
    pass


class GetLocalComponentsParams(BaseModel):
    """Parameters for get_local_components command."""
    pass


class GetInstanceOverridesParams(BaseModel):
    """Parameters for get_instance_overrides command."""
    instanceNodeId: Optional[str] = None


class ExportNodeAsImageParams(BaseModel):
    """Parameters for export_node_as_image command."""
    nodeId: str
    outputPath: str  # Required: full absolute path to output directory
    format: Optional[ExportFormat] = ExportFormat.PNG
    scale: Optional[float] = 1.0
    filename: Optional[str] = None


class JoinParams(BaseModel):
    """Parameters for join command."""
    channel: str


class ScanTextNodesParams(BaseModel):
    """Parameters for scan_text_nodes command."""
    nodeId: str
    useChunking: bool
    chunkSize: int


class GetAnnotationsParams(BaseModel):
    """Parameters for get_annotations command."""
    nodeId: Optional[str] = None
    includeCategories: Optional[bool] = False


class ScanNodesByTypesParams(BaseModel):
    """Parameters for scan_nodes_by_types command."""
    nodeId: str
    types: List[str]


class GetReactionsParams(BaseModel):
    """Parameters for get_reactions command."""
    nodeIds: List[str]


# Union type for all command parameters
CommandParams = Union[
    GetDocumentInfoParams,
    GetSelectionParams,
    GetNodeInfoParams,
    GetNodesInfoParams,
    ReadMyDesignParams,
    GetStylesParams,
    GetLocalComponentsParams,
    GetInstanceOverridesParams,
    ExportNodeAsImageParams,
    JoinParams,
    ScanTextNodesParams,
    GetAnnotationsParams,
    ScanNodesByTypesParams,
    GetReactionsParams,
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