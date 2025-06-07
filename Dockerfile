# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory to /admin_ui
WORKDIR /admin_ui

# Copy the current directory contents into the container at /admin_ui
COPY admin_ui .

# Install any needed packages specified in package.json
RUN npm install --no-audit --no-fund

# Expose port 3000
EXPOSE 3000

# Run npm run dev when the container launches
CMD ["npm", "run", "dev"]