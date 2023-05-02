import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.environ.get("API_BASE","https://framex-dev.wadrid.net/api/")
VIDEO_NAME = os.environ.get("VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c")


def startInteraction():
  """
    Gets the start bisection and image url. 
  """
  frames = getVideoInfo()["frames"]
  mid = bisect(frames)
  image_url = getImageUrl(mid)
  return {"left_frame":0, "right_frame":frames, "mid_frame": mid, "mid_frame_url": image_url}


def bisectFrame(left: int, right: int, mid: int, test: bool):
  """
  Rearrange the bisection ranges and gets a new mid frame number and image url.
  - `left` is the left frame number.
  - `right` is the right frame number.
  - `mid` is the mid frame number.
  - `test` is a flag that says if the mid frame is within the "right" range.
  """
  if test:
    right = mid
  else:
    left = mid

  if left + 1 < right:
    new_mid = bisect(right, left)
    image_url = getImageUrl(new_mid)
    return {"bisect_status": False, "left_frame":left, "right_frame":right, "mid_frame": new_mid, "mid_frame_url": image_url}
  else:
    image_url = getImageUrl(mid)
    return {"bisect_status": True, "left_frame":left, "right_frame":right, "mid_frame": mid, "mid_frame_url": image_url}


def bisect(right: int, left = 0):
  """
  Run a bisection
  - `right` is the right range
  - `left` is the left range
  """
  mid = int((left + right) / 2)
  return mid


def getVideoInfo():
  """
  Gets the information of the video
  """
  try:
    r = requests.get(f"{API_BASE}video/{VIDEO_NAME}")
  except Exception as e:
    print("Error at getting frame info" + str(e))

  if r.status_code == requests.codes.ok:
    return r.json()


def getImageUrl(frame: int):
  """
  Construct a frame url image
  - `frame` frame number
  """
  url = f"{API_BASE}video/{VIDEO_NAME}/frame/{frame}"
  return url

