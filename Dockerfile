# Use a lightweight Python image
FROM python:3.12-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into container
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
