# Migration Plan

This document tracks the migration progress from the original `code.js` to the new modular architecture.

## Migration Status

### ✅ Completed

#### Infrastructure
- [x] Project structure setup
- [x] TypeScript configuration
- [x] Webpack configuration
- [x] Constants extraction
- [x] Types definitions
- [x] Utilities extraction
- [x] Services setup
- [x] Main entry point

#### Commands
- [x] Document Commands
  - [x] get_document_info
  - [x] get_selection
  - [x] get_node_info

- [x] Create Commands
  - [x] create_rectangle
  - [x] create_frame

- [x] Style Commands (Partial)
  - [x] set_fill_color

### 🚧 In Progress

- [ ] Document Commands
  - [ ] get_nodes_info
  - [ ] read_my_design

### 📋 TODO

#### Commands to Migrate

1. **Create Commands**
   - [ ] create_text

2. **Style Commands**
   - [ ] set_stroke_color
   - [ ] set_corner_radius

3. **Transform Commands**
   - [ ] move_node
   - [ ] resize_node
   - [ ] clone_node

4. **Delete Commands**
   - [ ] delete_node
   - [ ] delete_multiple_nodes

5. **Text Commands**
   - [ ] set_text_content
   - [ ] scan_text_nodes
   - [ ] set_multiple_text_contents
   - [ ] setCharacters utility integration

6. **Component Commands**
   - [ ] get_styles
   - [ ] get_local_components
   - [ ] create_component_instance
   - [ ] get_instance_overrides
   - [ ] set_instance_overrides

7. **Layout Commands**
   - [ ] set_layout_mode
   - [ ] set_padding
   - [ ] set_axis_align
   - [ ] set_layout_sizing
   - [ ] set_item_spacing

8. **Export Commands**
   - [ ] export_node_as_image

9. **Annotation Commands**
   - [ ] get_annotations
   - [ ] set_annotation
   - [ ] scan_nodes_by_types
   - [ ] set_multiple_annotations

10. **Reaction Commands**
    - [ ] get_reactions

11. **Connection Commands**
    - [ ] set_default_connector
    - [ ] create_connections
    - [ ] createCursorNode helper

## Migration Guidelines

### When migrating a command:

1. **Create the command file** in the appropriate directory
2. **Add proper TypeScript types** for parameters and return values
3. **Extract any helper functions** to utilities
4. **Use services** for cross-cutting concerns (storage, progress)
5. **Add to exports** in the category index file
6. **Update command handler** to include the new command
7. **Test the command** to ensure it works correctly
8. **Update this file** to mark the command as completed

### Code Quality Checklist

- [ ] TypeScript types for all parameters
- [ ] Proper error handling with meaningful messages
- [ ] No direct figma API calls in services (pass as parameters if needed)
- [ ] Helper functions extracted to utilities
- [ ] Constants used instead of magic strings
- [ ] Documentation comments for complex logic
- [ ] Progress tracking for long-running operations

## Notes

- The `setcharacters.js` file needs to be converted to TypeScript and integrated into the text utilities
- Some commands have complex interdependencies that need careful handling during migration
- Progress tracking should be implemented as a middleware pattern in the command handler
- Consider creating a validation layer for command parameters