# Use an official Node.js runtime as a parent image
# Use a specific version to ensure consistency, e.g., 18-alpine
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
# This step is cached, so dependencies are only re-installed if these files change
COPY package.json ./

# Install dependencies
# Using 'npm ci' is recommended for CI/CD environments as it uses the lock file
# and is generally faster and more reliable for creating consistent builds.
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the Next.js application for production
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Define the command to start the application
# 'npm start' will run 'next start', which is the production server
CMD ["npm", "start"]
