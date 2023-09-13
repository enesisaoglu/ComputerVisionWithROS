import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
command_pub = rospy.Publisher("motor_commands", String)

def IsYellow(value):
    return value > 100
    

def Plan(left, right):
    COMMAND = "STOP"
    if IsYellow(left) and IsYellow(right):
       COMMAND = "GO"
    if IsYellow(left) and not IsYellow(right):
       COMMAND = "LEFT"
    if not IsYellow(left) and IsYellow(right):
       COMMAND = "RIGHT"
    print(left, right, COMMAND)
    command_pub.publish(COMMAND)
    return COMMAND
    
    
def ImageCallBack(data):
  cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
  # Width = 800, Height = 800...
  
  gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
  
  COMMAND = Plan(gray_image[700][300], gray_image[700][500])

  gray_image = cv2.line(gray_image, (300, 700), (500, 700), 0, 5 )
    
  if COMMAND == "LEFT":
     gray_image = cv2.circle(gray_image, (300, 700), 5, 255, 5)
  if COMMAND == "RIGHT":
     gray_image = cv2.circle(gray_image, (500, 700), 5, 255, 5)
  if COMMAND == "GO":
     gray_image = cv2.circle(gray_image, (400, 700), 5, 255, 5)

  cv2.imshow("Raw Image", gray_image)
  cv2.waitKey(3)
    
def main():
  print("Hey Universe!")
  rospy.init_node('my_planner_node')
  image_sub = rospy.Subscriber("/camera/image_raw",Image,ImageCallBack)
  rospy.spin()
  
if __name__ == "__main__":
  main()

