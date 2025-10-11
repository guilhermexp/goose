#!/bin/bash
# Start Goose Application - Backend + Frontend

# Kill any existing goosed process
pkill -f "target/release/goosed" 2>/dev/null

# Start backend in background
echo "Starting backend..."
cd /Users/guilhermevarela/Public/Goose
export GOOSE_PORT=3000
./target/release/goosed agent > /tmp/goosed.log 2>&1 &

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd /Users/guilhermevarela/Public/Goose/ui/desktop
npm run start-gui
