# Stage 1: Build dependencies
FROM node:18-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

# Stage 2: Runtime
FROM node:18-slim

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (res) => { if (res.statusCode === 200) process.exit(0); else process.exit(1); })"

CMD ["node", "app.js"]
