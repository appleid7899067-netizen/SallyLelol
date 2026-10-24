#!/bin/bash
# Test NovaDesign showcase via Browser MCP server
NODE_PATH=/data/data/com.termux/files/home/cow/browser-mcp-server/node_modules
export MCP_CONFIG_FILE=/data/data/com.termux/files/home/cow/mcp.json
node /data/data/com.termux/files/home/cow/browser-mcp-server/index.js 2>&1 | head -30
