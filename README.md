# Robot2025

This is the repository for FRC team 2813's code for our 2025 robot, Maelstørm.

## Cloning the Repository

There are two different ways to clone the robot code in order to work on it.
The only difference between the two is what protocol is used to communicate with GitHub.
The reccomended method is HTTPS (Hypertext Transfer Protocol Secure), which will work on school wifi.
The alternative is SSH (Secure Shell Protocol), which will not work on school wifi.
You only need to follow the instructions for cloning with one protocol

### Cloning with HTTPS

In order to clone the repository, with the `lib2813` submodule cloned as well.

```
git clone --recurse-submodules https://github.com/Prospect-Robotics/Robot2025.git
```

> [!NOTE]
> The `--recurse-submodules` can be omitted to only clone the `Robot2025` repo, and not the `lib2813` submodule.
> If the `lib2813` submodule is not present, the code will not build.

### Cloning with SSH

> [!CAUTION]
> Currently, a ssh robot code setup will not be able to access GitHub on school wifi due to the ssh port being used.
> If you plan to work on school wifi, you may want to consider using https.
> This does not apply with the Coder setup, as the machine that it is running on does not have the ssh port blocked, so you will be able to work with GitHub regardless of location, as long as you have internet access.

#### Setting up a SSH key

In order to be able to authenticate, you need to create a ssh key, and add the public fingerprint to GitHub.
If you already have a ssh key, you can skip this step.
To generate the key, you can run
```
ssh-keygen -t rsa -b 4090
```
and follow the prompts.
You can also create a different type of ssh key, or use the default number of bits.
See the [ssh-keygen man page](https://linux.die.net/man/1/ssh-keygen) for more information.

Then, you need to copy the contents of the public fingerprint (in the directory ~/.ssh by default).
The default name is `id_rsa`, so the command to copy it would be
```
# linux
cat ~/.ssh/id_rsa.pub | xclip -selection clipboard
# mac
cat ~/.ssh/id_rsa.pub | pbcopy
# windows
type ~\.ssh\id_rsa.pub | clip
```
> [!CAUTION]
> Do not give the contents of your private key to anyone!
> The file should have the same name as the public key, but without the .pub

Then, in GitHub settings, you can add an ssh key, and add your new key, and then authentication should work!
You can verfy it by running the following command, which should tell you your GitHub username if you are successfully authenticated.
```
ssh -T git@github.com
```

#### SSH Clone

For the clone and submodule setup, you can run the following commands

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

### Command line one-liner

> [!NOTE]
> This command is only tested under Linux and Mac, and will likely fail on Windows due to different functionality of the ping command.

In order to use this, you need to run it, and you will eventuall get a successful ping from 10.28.13.2 (roboRIO's ip address).
After that, you can press CTRL+C to cancel the ping, and start the deploy process.
If the deploy was successful, the terminal will be cleared, and if it fails, it will not be cleared, so you can see the error message.

```
ping 10.28.13.2; ./gradlew deploy && clear
```
