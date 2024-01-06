
#include <stdio.h>
#include "arm_ros_test.h"
#include "geometry_msgs/TwistStamped.h"
#include <moveit/move_group_interface/move_group_interface.h>

using namespace arm_ros;
#define SPD_SCL 0.5

//-----
bool ArmRosTest::test_arm_ros()
{
    ArmROS arm;
    arm.init();
    //----- set joints
    log_i("ArmROS set joints1...");
    ArmSt st;
    st.angles = {10,-5,-10,15,-20,30};
    arm.setJoints(st, 5);
    sys::sleep(2);
    //---
    log_i("ArmROS set joints2...");
    st.angles = {-10,5,10,-15,20,-30};
    arm.setJoints(st, 5);
    sys::sleep(2);

    //-----moveit
    log_i("ArmROS move to pose 1...");
    TipSt ts;
    ts.T.t = vec3(0.132, -0.150, 0.20);
    ts.T.q = quat(0.014, 0.026, 1.0, 0.0);// w,x,y,z
    arm.moveTo(ts);
    sys::sleep(5);
    log_i("ArmROS test done.");

    return true;
}

//-----
bool ArmRosTest::test_moveit_joints()
{
    moveit::planning_interface::MoveGroupInterface arm("arm_group");

    arm.setGoalJointTolerance(0.01);
    arm.setMaxVelocityScalingFactor(0.8);

    //----
    /*
    ROS_INFO("Moveing to init pose...");
    arm.setNamedTarget("init_pose");
    arm.move();
    ROS_INFO("done");
    */
    //----
    ROS_INFO("Moveing to joint-space goal: joint_positions");

    std::vector<double> arm_joint_positions = {0.9, -1.4, -0.7, 0.8, -0.5, -0.6};
    arm.setJointValueTarget(arm_joint_positions);
    arm.move();
    //-----
    // moveit::planning_interface::MoveGroupInterface::Plan plan;
   // bool success = (arm.plan(plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  //  ROS_INFO_NAMED("moveit_joint_pose_demo", "Visualizing plan 1 (joint space goal) %s", success ? "" : "FAILED");
  //  if(success){
  //      arm.execute(plan);
  //  }
    //-----    
    return true;
}
//-----
bool ArmRosTest::test_moveit_grip()
{
    moveit::planning_interface::MoveGroupInterface grip("gripper");

    grip.setGoalJointTolerance(0.01);
    grip.setMaxVelocityScalingFactor(0.8);

    //----
    /*
    ROS_INFO("Moveing to init pose...");
    arm.setNamedTarget("init_pose");
    arm.move();
    ROS_INFO("done");
    */
    //----
    ROS_INFO("Moveing to joint-space goal: joint_positions");

    grip.setJointValueTarget({toRad(-40)});
    grip.move();
    sys::sleep(2);
    //----
    grip.setJointValueTarget({toRad(10)});
    grip.move();
    sys::sleep(2);
    //-----
    grip.setJointValueTarget({toRad(-40)});
    grip.move();
    sys::sleep(2);
    //-----
    // moveit::planning_interface::MoveGroupInterface::Plan plan;
   // bool success = (arm.plan(plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  //  ROS_INFO_NAMED("moveit_joint_pose_demo", "Visualizing plan 1 (joint space goal) %s", success ? "" : "FAILED");
  //  if(success){
  //      arm.execute(plan);
  //  }
    //-----    
    return true;
}

//-----
bool ArmRosTest::test_moveit_pose()
{
    
    //--------------------

    // 创建对象arm连接到xarm规划组
    moveit::planning_interface::MoveGroupInterface arm("arm_group");
    // 获取xarm规划组的规划参考坐标系
    std::string sFrm = arm.getPlanningFrame();
    ROS_INFO_STREAM("get planning frame : "<< sFrm);
    arm.setPoseReferenceFrame("g_base");
    // 获取末端执行器的link
    std::string s_eefLnk = arm.getEndEffectorLink();
    ROS_INFO_STREAM("get End effector link : "<< s_eefLnk);
    arm.setEndEffectorLink(s_eefLnk);

    // 若allow_replanning()参数为True，则MoveIt!在一次规划失败后进行重新规划
    arm.allowReplanning(true);
    // 设置运动到目标时的位置(单位：米)和姿态的容忍误差(单位：弧度)
    arm.setGoalPositionTolerance(0.01);
    arm.setGoalOrientationTolerance(0.05);
    // 设置一个比例因子以选择性地降低最大关节速度限制，可取值为(0,1]
    arm.setMaxVelocityScalingFactor(SPD_SCL);
    log_i("init moveit done");    
    sys::sleep(2);
    //------
    log_i("go init pose...");
    arm.setNamedTarget("init_pose");
    arm.move();
    log_i("done");
    sys::sleep(5);

   
    
    //---------------
    // 使用geometry_msgs/PoseStamped消息类型设置机械臂的目标位姿
    geometry_msgs::PoseStamped target_pose; 
    //----
    target_pose.header.frame_id = sFrm;
    target_pose.header.stamp = ros::Time::now();


    /* // 1)-------------
    target_pose.pose.position.x = 0.3;
    target_pose.pose.position.y = -0.3;
    target_pose.pose.position.z = 0.25;
    tf2::Quaternion quaternion;
    quaternion.setRPY(0, 3.1415926/2.0,0);
    target_pose.pose.orientation.x = quaternion.x();
    target_pose.pose.orientation.y = quaternion.y();
    target_pose.pose.orientation.z = quaternion.z();
    target_pose.pose.orientation.w = quaternion.w();
    */ //----------------

    target_pose.pose.position.x = 0.132;
    target_pose.pose.position.y = -0.150;
    target_pose.pose.position.z = 0.20;

    target_pose.pose.orientation.w = 0.014;
    target_pose.pose.orientation.x = 0.026;
    target_pose.pose.orientation.y = 1.0;
    target_pose.pose.orientation.z = 0.0;

    //------------------
    // 显示地把开始状态设置为机械臂的当前状态
    arm.setStartStateToCurrentState();
    ROS_INFO("Moving to target_pose ...");
    // 设置目标位姿
    arm.setPoseTarget(target_pose);
    // 使用plan()进行运动规划
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    bool success = (arm.plan(plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
    ROS_INFO_NAMED("moveit_pose_demo", "Visualizing plan 1 (joint space goal) %s", success ? "" : "FAILED");
    // 若规划成功,则使用execute()执行规划出的轨迹
    if(success){
        arm.execute(plan);
    }
    log_i("done");
     //---------------
    sys::sleep(5);
  
    log_i("gettting current pose...");
    geometry_msgs::PoseStamped pose; 
    pose = arm.getCurrentPose();
    stringstream s;
    s << "  pos: ( " << pose.pose.position << "), " << endl;
    s << "  quat: ( " << pose.pose.orientation << " )" << endl;
    log_i(s.str());
    log_i("gettting current pose done.");
    return true;
}
//-------------
// run()
//-------------
void ArmRosTest::run()
{   
    ros::AsyncSpinner spinner(1);
    spinner.start();
    
    string s = "arm_ros_test node started...";
    s += "CurDir:"+ sys::pwd();
    ut::log_i(s);
    //----
    //test_moveit_joints();
    test_moveit_grip();
    //test_moveit_pose();
    //test_arm_ros();

    //-------------------
    //---- test chatter
    //  ros::Subscriber subCmd = 
    //    nh_.subscribe(lc_.topic.cmd, 1000, vrp_cmd_cb);

    //---- publisher
    //pub_ = nh_.advertise<std_msgs::String>(lc_.topic.vision, 1000);


    //---- ROS mainloop
    log_d("ros spin...");
    ros::spin();
    log_d("ros spin done.");


}


//------------
// main
//------------

int main(int argc, char **argv)
{
  using namespace std;
  ros::init(argc, argv, "arm_ros_test");

  ArmRosTest nn;
  nn.run();
  return 0;
}
