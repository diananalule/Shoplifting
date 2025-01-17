## Shoplifting Detection System

## Overview
This project introduces an AI-powered surveillance system designed to detect and prevent shoplifting in supermarkets. By integrating **Artificial Intelligence** (AI) algorithms with existing **CCTV systems**, the solution automates real-time detection of suspicious activities, minimizing human error and enhancing security. The system utilizes **Convolutional Neural Networks (CNNs)** trained with **transfer learning** to recognize abnormal behaviors, specifically focused on shoplifting incidents.

## Features
- **Real-Time Surveillance**: Processes live video footage from CCTV cameras to detect suspicious activities instantly.
- **Automated Alert System**: Sends real-time notifications when shoplifting or unusual behavior is detected.
- **Transfer Learning Integration**: Utilizes pre-trained CNN models (e.g., ResNet50) to reduce training time and improve detection accuracy.
- **Efficient Performance**: Runs on regular CPUs with minimal processing time compared to GPU-based systems.

## Table of Contents
1. [Background](#background)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Scope](#scope)
5. [Significance](#significance)
6. [Technology Stack](#technology-stack)
7. [Project Collaborators](#Project-Collaborators)
  

## Background
In today’s evolving business landscape, the need for secure retail environments is critical. Existing surveillance systems, such as **CCTV** and **Electronic Article Surveillance (EAS)**, often fail to detect sophisticated shoplifting activities. This project addresses this issue by incorporating AI-powered **Convolutional Neural Networks (CNNs)**, developed using **transfer learning**, to analyze video footage for suspicious behaviors in real time.

## Problem Statement
Current security systems are inadequate for identifying advanced shoplifting techniques. Traditional CCTV systems rely heavily on human operators and are prone to error, while EAS systems are bypassed easily. The lack of automated, proactive detection systems in supermarkets leads to significant financial losses globally.

## Objectives
### Main Objective
To revolutionize supermarket security by integrating AI-powered surveillance systems that automatically detect and alert for shoplifting activities.

### Specific Objectives
1. Collect video and image data representing shoplifting incidents and normal supermarket activities.
2. Develop machine learning models to detect shoplifting via scene analysis.
3. Evaluate model performance using confusion matrices and select the best-performing model.
4. Develop a real-time shoplifting detection and alert system.

## Scope
This project focuses on developing an AI-enhanced security system within supermarkets. It utilizes **CCTV cameras** to collect video data, which is then processed through **Convolutional Neural Networks (CNNs)**, trained via **transfer learning** to recognize shoplifting activities. The system aims to offer automated alerts and improve store security.

The research is limited to the supermarket environment, using real-time video feeds, with potential scalability to other retail environments in the future.

## Significance
### Academic Significance
This research advances the field of AI in security systems by employing deep learning techniques for anomaly detection in retail environments. It contributes valuable insights into AI's role in enhancing surveillance technologies and improving security.

### Practical Significance
The system addresses the limitations of existing security measures and provides a more effective solution for shoplifting detection. By automating alerts and reducing the need for manual monitoring, the system enhances store security, reduces losses, and provides a safer shopping environment for customers and staff.

## Technology Stack
- **Backend**: Django (Python), OpenCV, TensorFlow, PyTorch
- **Machine Learning**: Transfer Learning with pre-trained **ResNet50** CNN model
- **Video Processing**: OpenCV for real-time video analytics
- **Database**: SQLite for storing event logs and detection alerts
- **Deployment**: Docker, Heroku for cloud deployment
- **Other Libraries**: NumPy, Matplotlib, Pillow, Roboflow
- # Project Collaborators

This project would not have been possible without the dedication and hard work of the following collaborators:

- **Nalule Diana**: Contributed to  Data collection, preprocessing, and model evaluation.
- **Basiima Collinelius**: Worked on  system architecture and integration.
- **Katalemwa Javious (You)**: Led the development and implementation of AI-based security solutions, overseeing the integration of Convolutional Neural Networks for anomaly detection.
- **Nakalanzi Vivian**: Focused on, alert system development and user interface design.

Together, we have created an innovative solution for detecting shoplifting in supermarkets using AI-enhanced surveillance.




###  Clone the repository:

git clone https://github.com/diananalule/Shoplifting.git
