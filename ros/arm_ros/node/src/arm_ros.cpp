#include <stdio.h>
#include "arm_ros.h"

using namespace arm_ros;

bool ArmROS::init()
{
    log_i("ArmROS init MoveIt...");    

    p_arm_  = mkSp<moveit::planning_interface::MoveGroupInterface>(cfg_.sGroup);
    p_grip_ = mkSp<moveit::planning_interface::MoveGroupInterface>(cfg_.sGrip);
    auto& arm = * p_arm_;
    arm.allowReplanning(true);
    arm.setPoseReferenceFrame(cfg_.sPoseRefFrm);
    arm.setGoalPositionTolerance(cfg_.goalToler.pos);
    arm.setGoalOrientationTolerance(cfg_.goalToler.orien);
    arm.setMaxVelocityScalingFactor(cfg_.max_spd_scl);

    auto& grip = *p_grip_;
    grip.setGoalJointTolerance(cfg_.grip.toler);
    grip.setMaxVelocityScalingFactor(cfg_.max_spd_scl);
    log_i("  init MoveIt done");    

    return true;
}
//-----
bool ArmROS::setJoints(const ArmSt& st, double spd)
{
    if(!chkInit()) return false;
    auto& arm = * p_arm_;

    arm.setMaxVelocityScalingFactor(spd);

    //std::vector<double> arm_joint_positions = {0.9, -1.4, -0.7, 0.8, -0.5, -0.6};
    vector<double> js;
    for(auto& j : st.angles)
        js.push_back(toRad(j));
    arm.setJointValueTarget(js);
    arm.move();
    return true;
}
//----
bool ArmROS::setGrip(double d, double spd)
{
    if(!chkInit()) return false;
    const float& a0 = cfg_.grip.dgr_open;
    const float& a1 = cfg_.grip.dgr_close;
    float a = a0 + (a1 - a0)*d;
    log_d("  set grip :"+ str(a));
    //---
    auto& grip = *p_grip_;
    grip.setMaxVelocityScalingFactor(spd);
    grip.setJointValueTarget({toRad(a)});
    grip.move();
    return true;
}

//----
bool ArmROS::moveTo(const TipSt& ts, float spd)
{
    if(!chkInit()) return false;
    auto& arm = * p_arm_;
    arm.setMaxVelocityScalingFactor(spd);

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
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    bool ok = (arm.plan(plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
    if(!ok)
    {
        log_e("ArmROS::moveTo() Planning failed.");
        return false;
    }
    
    arm.execute(plan);
    
    return true;

}
//----

//-----
bool ArmROS::getSt(ArmSt& st)
{
    if(!chkInit()) return false;
    auto& arm = * p_arm_;
    auto psm = arm.getCurrentPose();
    auto p = psm.pose.position;
    auto o = psm.pose.orientation;
    st.tip.T.t << p.x,p.y,p.z;
    st.tip.T.q = quat(o.w,o.x,o.y,o.z);
    auto rs = arm.getCurrentJointValues();
    for(auto& r : rs)
        st.angles.push_back(toDgr(r));

    return true;

}
