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
        quat q;
        //Euler e;
        
        string str()const ;
        //bool set(const string& s);
        /*
        void operator += (const Trans& T)
        { 
            e += T.e;
            t += T.t;
        }
        */
    };
    //----------
    struct TipSt{
        Trans T;
        double gripper = 0;
        string str()const;
    };
    //---
    /*
    struct JointSt{
        double r=0; // angle in degree
        // other status, acc, rot speed etc
    };
    */
    //-----
    struct ArmSt{
        TipSt tip;
        vector<double> angles;
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
        virtual bool setGrip(double d, double spd=1.0){ return true; }
        virtual bool setJoints(const ArmSt& st, double spd=1.0){  return true; };
        virtual bool moveTo(const TipSt& ts, float spd=1.0){  return true; };
        virtual bool getSt(ArmSt& st) { return false; }
        virtual bool play(const string& sf){ return false; };
        virtual bool test(){ return false; };

        // TODO: busy()
        virtual bool done()const{return true;};
        
        //---- factory 
        static Sp<Arm> create(const string& sModel);
        //--- creators for factory 
        using FuncCre = std::function<Sp<Arm>()>;
        static void addCreator(const string& sModel,
                               FuncCre f);

        //---- grab a place, with Pose,
        // dt0 is offset for approach point
        bool grab(const Trans& T_target,
                  const vec3& dt0);
        void waitDone();

    };
    //--------
    // ArmMng
    //--------
    class ArmMng : public Cmd
    {
    public:
        ArmMng();

        auto getArm(){ return p_arm_; }
        void set(Sp<Arm>p)
        { p_arm_ = p; data_.hasInit = true; }
    protected:
        struct Data{
            bool hasInit = false;
        }; Data data_;
        Sp<Arm> p_arm_ = nullptr;

        void init_cmds();
         
        bool init(CStrs& args);
        bool client(CStrs& args);
        bool setJoints(CStrs& args);
        bool setGrip(CStrs& args);
        bool moveto(CStrs& args);
        bool grab(CStrs& args);
        bool checkInit();
        bool getSt();
        bool play(const string& sf);

        bool chkInit()const;
    };
}
