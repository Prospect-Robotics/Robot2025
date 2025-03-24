# Robot2025

![Tests Passing?](https://github.com/Prospect-Robotics/Robot2025/actions/workflows/gradle.yml/badge.svg)

This is the repository for FRC team 2813's code for our 2025 robot, Maelstørm.

## Cloning the Repository

There are two different ways to clone the robot code in order to work on it.
The only difference between the two is what protocol is used to communicate with GitHub.
The recommended method is HTTPS (Hypertext Transfer Protocol Secure), which will work on school WiFi.
The alternative is SSH (Secure Shell Protocol), which will not work on school wifi.
You only need to follow the instructions for cloning with one protocol

### Pre-Clone Setup

If you haven't cloned with HTTPS or SSH before, you need to set them up first.
See the documentation for the [HTTPS setup](https://github.com/git-ecosystem/git-credential-manager/tree/release), and the [SSH Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).


### Cloning with HTTPS

In order to clone the repository, with the `lib2813` submodule cloned as well, run:

```
git clone --recurse-submodules https://github.com/Prospect-Robotics/Robot2025.git
```

> [!NOTE]
> The `--recurse-submodules` can be omitted to only clone the `Robot2025` repo, and not the `lib2813` submodule.
> If the `lib2813` submodule is not present, the code will not build.

### Cloning with SSH

> [!CAUTION]
> Currently, a SSH robot code setup will not be able to access GitHub on school wifi due to the SSH port being used.
> If you plan to work on school wifi, you may want to consider cloning with HTTPS.
> This does not apply with the Coder setup, as the machine that it is running on does not have the SSH port blocked, so you will be able to work with GitHub regardless of location, as long as you have internet access.

For the clone and submodule setup, you can run the following commands:

> [!NOTE]
> Anything after a hashtag (#) is a comment, and does not need to be put in.
If you do put them in, they will be ignored by the terminal.

```
git clone git@github.com:Prospect-Robotics/lib2813.git # clone repo with ssh (submodule not initialized)
git submodule init lib2813 # initialize the lib2813 submodule
git config submodule.lib2813.url git@github.com:Prospect-Robotics/lib2813.git # Set the submodule url to use ssh instead of the default https
git submodule update # check out the correct commit in the lib2813 submodule
```

## Deploying to the robot

### Command line

To deploy from the command line you can run the following command while in the directory you have cloned the repository
```
# linux & mac
./gradlew deploy
# windows
.\gradlew.bat deploy
```
You must be connected to the robot's network in order to deploy (robot wifi, ethernet, or a USB-B cable).

### Command line one-liner

> [!NOTE]
> This command is only tested under Linux and Mac, and will fail on Windows due to the Windows ping command not pinging infinitely.

In order to use this, you need to run it, and you will eventually get a successful ping from 10.28.13.2 (roboRIO's ip address).
After that, you can press CTRL+C to cancel the ping, and start the deploy process.
If the deploy was successful, the terminal will be cleared, and if it fails, it will not be cleared, so you can see the error message.

```
ping 10.28.13.2; ./gradlew deploy && clear
```
