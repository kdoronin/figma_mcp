# Cursor MCP Plugin - Refactored Architecture

This Figma plugin has been refactored to follow a modular architecture with clear separation of concerns and TypeScript support.

## Project Structure

```
src/cursor_mcp_plugin/
├── src/                        # Source code
│   ├── main.ts                # Main entry point
│   ├── commands/              # Command implementations
│   │   ├── document/          # Document-related commands
│   │   ├── create/            # Creation commands
│   │   └── ...                # Other command groups
│   ├── handlers/              # Request handlers
│   │   └── commandHandler.ts  # Main command dispatcher
│   ├── services/              # Business logic services
│   │   ├── progress.service.ts
│   │   └── storage.service.ts
│   ├── utils/                 # Utility functions
│   │   ├── helpers.ts
│   │   └── node-filters.ts
│   ├── types/                 # TypeScript type definitions
│   │   └── index.ts
│   └── constants/             # Constants and enums
│       └── index.ts
├── dist/                      # Compiled output
│   └── code.js               # Bundled plugin code
├── ui.html                    # Plugin UI
├── manifest.json              # Plugin manifest
├── package.json               # Node dependencies
├── tsconfig.json              # TypeScript config
└── webpack.config.js          # Webpack bundler config
```

## Architecture Overview

### 1. **Main Entry Point** (`src/main.ts`)
- Initializes the plugin
- Sets up UI communication
- Handles message routing
- Manages plugin state

### 2. **Commands** (`src/commands/`)
- Organized by functionality (document, create, style, etc.)
- Each command is a separate function
- Follows Single Responsibility Principle
- Easy to add new commands

### 3. **Handlers** (`src/handlers/`)
- `commandHandler.ts` - Main command dispatcher
- Routes commands to appropriate implementations
- Handles error handling and validation

### 4. **Services** (`src/services/`)
- `ProgressService` - Manages progress tracking for long operations
- `StorageService` - Handles plugin settings and storage
- Business logic separated from commands

### 5. **Utilities** (`src/utils/`)
- Helper functions for common operations
- Node filtering and transformation
- Base64 encoding, color conversion, etc.

### 6. **Types** (`src/types/`)
- TypeScript interfaces and types
- Centralized type definitions
- Improves code maintainability

### 7. **Constants** (`src/constants/`)
- All constants in one place
- Command names, message types, etc.
- Easy to maintain and update

## Development

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Setup
```bash
npm install
```

### Build
```bash
# Production build
npm run build

# Development build with watch
npm run watch

# Single development build
npm run dev
```

### Adding New Commands

1. Create a new file in the appropriate command directory:
```typescript
// src/commands/myCategory/myCommand.ts
/// <reference types="@figma/plugin-typings" />

export async function myCommand(params: any) {
  // Implementation
  return result;
}
```

2. Export from the category index:
```typescript
// src/commands/myCategory/index.ts
export { myCommand } from './myCommand';
```

3. Add to constants:
```typescript
// src/constants/index.ts
export const COMMANDS = {
  // ...
  MY_COMMAND: 'my_command',
};
```

4. Add to command handler:
```typescript
// src/handlers/commandHandler.ts
case COMMANDS.MY_COMMAND:
  return await myCommand(params);
```

## Benefits of This Architecture

1. **Modularity**: Each piece has a single responsibility
2. **Scalability**: Easy to add new features without touching existing code
3. **Maintainability**: Clear structure makes it easy to find and fix issues
4. **Type Safety**: Full TypeScript support with proper types
5. **Testability**: Separate functions are easier to unit test
6. **Performance**: Webpack bundles only what's needed

## Migration from Original Code

The original `code.js` file has been split into multiple modules:
- Document commands → `src/commands/document/`
- Create commands → `src/commands/create/`
- Style commands → `src/commands/style/`
- Text commands → `src/commands/text/`
- Component commands → `src/commands/component/`
- etc.

The migration is ongoing. Commands are being moved gradually to maintain stability.

## Future Improvements

1. Add unit tests for all commands
2. Implement error boundaries
3. Add logging service
4. Create command validation schemas
5. Add command middleware support
6. Implement command queuing for better performance