## Building STM32 Source Code in /moss_v1

Note: These must be run in the msys bash terminal

Set Environment Variables:
```$ source ~/.bashrc```

Check Environment Variables:
```$ "$CC" --version ```
```$ "$CXX" --version ```

Configure CMake:
```$ cmake -S /c/Users/asmig/GitProjects/quasaris_moss/moss_v1   -B /c/Users/asmig/GitProjects/quasaris_moss/moss_v1/build   -G "Unix Makefiles"   -DCMAKE_TOOLCHAIN_FILE=/c/Users/asmig/GitProjects/quasaris_moss/moss_v1/cmake/gcc-arm-none-eabi.cmake \         -DCMAKE_C_COMPILER=/c/PROGRA~2/ARMGNU~1/14.3RE~1/bin/arm-none-eabi-gcc.exe   -DCMAKE_CXX_COMPILER=/c/PROGRA~2/ARMGNU~1/14.3RE~1/bin/arm-none-eabi-g++.exe```

Build Project:
```$ cmake --build /c/Users/asmig/GitProjects/quasaris_moss/moss_v1/build```

Clean Project:
```$ rm -rf /c/Users/asmig/GitProjects/quasaris_moss/moss_v1/build/*```