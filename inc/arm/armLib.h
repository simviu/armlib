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
        string str()const // json str
        { return "{t:\""+vsn::str(t,3)+"\", ypr:\"" +e.str()+"\"}";  }
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
        double r=0;
        // other status, acc, rot speed etc
    };
    //-----
    struct ArmSt{
        TipSt tip;
        vector<JointSt> joints;
        string str()const{
            return "{ tip:"+tip.str() + "}";
        }
    };
    //----------
    // Arm
    //----------
    class Arm{
    public:
        struct Cfg{
            float maxSpeed = 1;
        }; Cfg cfg_;
        //----
        virtual bool init(){ return true; };
        virtual bool release(){ return true; };
        virtual bool reset(){  return true; };
        virtual bool moveTo(const TipSt& ts, float spd=1.0){  return true; };
        virtual bool getSt(ArmSt& st) { return false; }

        //---- factory 
        static Sp<Arm> create(const string& sModel);
        virtual bool test(){ return false; };
     //   virtual bool done()const=0;
    };
    //--------
    // ArmCmd
    //--------
    class ArmCmd : public Cmd
    {
    public:
        ArmCmd();

    protected:
        bool moveto(CStrs& args);
        bool run_server(CStrs& args);
        struct Data{
            string s_jres; // cmd result json string
        }; Data data_;
        Sp<Arm> p_arm_ = nullptr;
        bool checkInit(CStrs& args);
    };
}
