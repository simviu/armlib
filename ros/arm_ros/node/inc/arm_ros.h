#pragma once

#include "vsn/vsnLib.h"
#include "arm/armLib.h"

#include "ros/ros.h"
#include "std_msgs/String.h"

#include "geometry_msgs/TwistStamped.h"
#include <moveit/move_group_interface/move_group_interface.h>

namespace arm_ros{
    using namespace std;
    using namespace ut;
    using namespace arm;
    //---------
    // ROS move it
    class ArmROS : public Arm
    {
    public:
        struct Cfg{
            string sGroup = "arm_group";
            string sGrip = "gripper";
            string sPoseRefFrm = "g_base";
            float max_spd_scl = 0.8;
            //---
            float grip_min = -39;
            float grip_max = 9;
            float grip_toler = 0.01;
            //---
            struct GoalToler{
                float pos = 0.01;
                float orien = 0.05;
            }; GoalToler goalToler;
        }; Cfg cfg_;
        virtual bool init()override;
        virtual bool setJoints(const ArmSt& st, double spd=1.0)override;
        virtual bool setGrip(double d, double spd=1.0)override;
        virtual bool moveTo(const TipSt& ts, float spd=1.0)override;
        virtual bool getSt(ArmSt& st) override;
        virtual bool test()override{ return false; };
        virtual bool done()const override{ return false; };  

    protected:      
        Sp<moveit::planning_interface::MoveGroupInterface> 
            p_arm_ = nullptr;
        Sp<moveit::planning_interface::MoveGroupInterface> 
            p_grip_ = nullptr;            
        //---
        bool chkInit()const
        {
            if( (p_arm_ !=nullptr) &&
                (p_grip_!=nullptr) )return true;
            log_e("Arm not init");
            return false;
        }
    };
    //----- ArmROS_svr
    class ArmROS_svr : public ArmMng{
    public:
        bool init();
        
    protected:

    }; 
    
}
