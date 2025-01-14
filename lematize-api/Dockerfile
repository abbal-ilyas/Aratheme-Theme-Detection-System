# Use OpenJDK image as  base
FROM openjdk:17-jdk-alpine

# Copy the Rest API in the container
COPY  ./Rest-API-LemmaRootStem.jar LemmaRootStem.jar

# Expose the port used by the application 
EXPOSE 8081

# Command to run your application when the container starts
CMD ["java", "-jar", "LemmaRootStem.jar"]
