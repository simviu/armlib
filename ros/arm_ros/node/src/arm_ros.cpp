#include <stdio.h>
#include "arm_ros.h"

using namespace arm_ros;

bool ArmROS::init()
{
    log_i("ArmROS init MoveIt...");    

    p_arm_ = mkSp<moveit::planning_interface::MoveGroupInterface>(cfg_.sGroup);
    auto& arm = * p_arm_;
    arm.allowReplanning(true);
    arm.setPoseReferenceFrame("g_base");
    arm.setGoalPositionTolerance(cfg_.goalToler.pos);
    arm.setGoalOrientationTolerance(cfg_.goalToler.orien);
    arm.setMaxVelocityScalingFactor(cfg_.max_spd_scl);
    log_i("  init MoveIt done");    

    return true;
}
//-----
bool ArmROS::setJoints(const ArmSt& st, double t)
{
    if(!chkInit()) return false;
    auto& arm = * p_arm_;

    //std::vector<double> arm_joint_positions = {0.9, -1.4, -0.7, 0.8, -0.5, -0.6};
    vector<double> js;
    for(auto& j : st.angles)
        js.push_back(toRad(j));
    arm.setJointValueTarget(js);
    arm.move();
    return true;
}
//----
bool ArmROS::moveTo(const TipSt& ts, float spd)
{
    if(!chkInit()) return false;
    auto& arm = * p_arm_;

    //-----
    arm.setStartStateToCurrentState();
    log_i("  moving to p ...");

    //-----
    string sFrm = arm.getPlanningFrame();
    geometry_msgs::PoseStamped ps; 
    //----
    ps.header.frame_id = sFrm;
    ps.header.stamp = ros::Time::now();
    //--- pos
    auto& p = ps.pose.position;
    auto& t = ts.T.t;
    p.x = t.x(); 
    p.y = t.y();
    p.z = t.z();

    //--- orient
    auto& o =  ps.pose.orientation;
    auto& q = ts.T.q;
    o.w = q.w();
    o.x = q.x();
    o.y = q.y();
    o.z = q.z();

    arm.setPoseTarget(ps);

    return true;

}
//----

//-----
bool ArmROS::getSt(ArmSt& st)
{
    if(!chkInit()) return false;
    auto& arm = * p_arm_;

    return false;

}
