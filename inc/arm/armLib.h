/*
   Author: Sherman Chen
   Create Time: 2022-11-04
   Email: schen@simviu.com
   Copyright(c): Simviu Inc.
   Website: https://www.simviu.com
 */

#pragma once

#include <stdio.h>
#include <iostream>
#include "vsn/vsnLib.h"


namespace arm{
    using namespace std;
    using namespace ut;
    using namespace egn;
    using namespace vsn;

    //----------
    struct Trans{
        Trans(){ t << 0,0,0; }
        vec3 t;
        Euler e;
        
        string str()const ;
        bool set(const string& s);
        void operator += (const Trans& T)
        { 
            e += T.e;
            t += T.t;
        }
    };
    //----------
    struct TipSt{
        Trans T;
        double gripper = 0;
        string str()const 
        { return "{T:"+ T.str() + ", gripper:"+vsn::str(gripper) +"}"; }
    };
    //---
    struct JointSt{
        double r=0; // angle
        // other status, acc, rot speed etc
    };
    //-----
    struct ArmSt{
        TipSt tip;
        vector<JointSt> joints;
        string str()const;
    };
    //----------
    // Arm
    //----------
    class Arm{
    public:
        struct Cfg{
            float maxSpeed = 1;
            float dfltSpeed = 1;
        }; Cfg cfg_;
        //----
        virtual bool init(){ return true; };
        virtual bool release(){ return true; };
        virtual bool reset(){  return true; };
        virtual bool moveTo(const TipSt& ts, float spd=1.0){  return true; };
        virtual bool getSt(ArmSt& st) { return false; }
        virtual bool play(const string& sf){ return false; };
        virtual bool test(){ return false; };
        virtual bool done()const{return true;};
        //---- factory 
        static Sp<Arm> create(const string& sModel);
        //---- grab a place, with Pose,
        // dT0 is offset for approach point
        bool grab(const Trans& T_target,
                  const Trans& dT0);
        void waitDone();

    };
    //--------
    // ArmCmd
    //--------
    class ArmCmd : public Cmd
    {
    public:
        ArmCmd();

        bool init(CStrs& args);
    protected:
        struct Data{
            bool hasInit = false;
        }; Data data_;
        Sp<Arm> p_arm_ = nullptr;

        bool moveto(CStrs& args);
        bool grab(CStrs& args);
        bool checkInit();
        bool getSt();
        bool play(const string& sf);
    };
}
