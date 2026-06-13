# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /airline-analysis

# Copy the current directory contents into the container at /app
COPY . /airline-analysis

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port number
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "Airlines_analysis.py"]
