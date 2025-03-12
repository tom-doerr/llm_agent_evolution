# Project Notes

## Architecture Decisions
- Isolated CLI commands in separate module
- Introduced factory pattern for component creation
- Converted configs to Pydantic models for validation
- Separated command implementations from CLI definition

## Current Issues
1. Need validation tests for config models
2. Factory should support custom component injection
3. CLI command tests missing

## Next Steps
1. Add pytest for CLI commands
2. Implement config validation tests
3. Create dependency injection system
