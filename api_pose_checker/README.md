# Pose Angle Detection API

This is a FastAPI-based application for detecting and analyzing human body joint angles from images using MediaPipe. The app can compare poses to reference images and visualize selected joint angles.

## Features

- Detects body landmarks using MediaPipe.
- Calculates angles for various joints (elbow, hip, knee, etc.).
- Compares user pose with reference poses.
- Returns angle differences and annotated images.
- Includes a simple HTML frontend (`index.html`).

## Endpoints

### `POST /upload-photo`

Uploads an image and returns either:
- Annotated image with selected joint angles, or
- Comparison results with reference poses.

**Request Body (JSON):**
json
{
  "image": "data:image/png;base64,...",
  "name": "1" | "2" | "3" | any other string,
  "angle": int (bitmask for selected joints)
}
