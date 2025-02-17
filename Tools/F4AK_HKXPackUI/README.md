## About this fork

This fork was created to provide an update specifically for `F4AK_HKXPackUI` to support members of the [Collective Modding Discord](https://discord.gg/tktyEyYHZH) Community.  

This `F4AK_HKXPackUI` release is built upon [v1.0.5 from Nexus Mods](https://www.nexusmods.com/fallout4/mods/16694).  
It's been updated to Python 3 to resolve issues with file encodings, specifically these two errors:

```
File "F4AK_HKXPackUI\f4ak_hkxpack_UI.py", line 174, in convertHkxToFBXAnimation
LookupError: unknown encoding: cp65001
```

```
---------------------------
Microsoft Visual C++ Runtime Library
---------------------------
Runtime Error!
Program: f4ak_hkxpack_UI.exe
R6034
An application has made an attempt to load the C runtime library incorrectly.
Please contact the application's support team for more information.
```

Latest Release: [Download](https://github.com/wxMichael/ShadeAnimator_Fallout4_AnimationKit/releases/latest/download/f4ak_hkxpack_UI.exe)

The updated source code is [here](https://github.com/wxMichael/ShadeAnimator_Fallout4_AnimationKit/tree/master/Tools/F4AK_HKXPackUI).  
You can compare my changes to the v1.0.5 Nexus release [here](https://github.com/wxMichael/ShadeAnimator_Fallout4_AnimationKit/compare/36eb432...e605945#files_bucket).

[<img src="https://i.postimg.cc/dttk8WxL/CM-External-Banner-01.png">](https://discord.gg/tktyEyYHZH)

> [!IMPORTANT]
> Anti-virus may incorrectly flag the exe based on machine learning heuristics.  
Unfortunately this is very common with Python apps compiled to exe. Please allow sample submission if your AV asks so it can hopefully be marked safe.
VirusTotal analysis here:  
https://www.virustotal.com/gui/file/10e7b5d99d388380878559e1f5a7238e218160239eef530017f41e299a8e3e74 
