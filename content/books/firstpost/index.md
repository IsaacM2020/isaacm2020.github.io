---
title: Setting Up The Blog
date: 2024-12-09
draft: false
tags:
  - firstpost
  - blog
  - project37
---


A few years ago, I watched a video by Ali Abdaal regarding setting up a newsletter. This piqued my interest in the idea of blogging. I started blogging on substack for a few months but I stopped as I lost interest. However, around two weeks ago. Network Chuck, a tech education youtuber, posted a video on how you can create a blog, and host it on a custom domain. This caught my attention, as making a website could be a worthy challenge and would serve me well in the future. The tutorial by Network Chuck was a great start to the website, but did not provide an in-depth way of customizing the website. The purpose of this article is to help individuals not make the same mistakes that I made while trying to make this website.


I decided to start this project of making a blog, for the following reasons:
1. Having a blog is cool
2. It is fun to post your thoughts online
3. I wanted to use my (free) custom domain name
4. I wanted to learn how to build and host a website for free and from scratch


Step 1: Get all of your prerequisites ready

- Download Obsidian (a note taking tool) from https://obsidian.md/
- Download Git from [https://github.com/git-guides/install-git](https://github.com/git-guides/install-git)
- Download Go from [https://go.dev/dl/](https://go.dev/dl/)
- Download Hugo from [https://gohugo.io/installation/](https://gohugo.io/installation/) - Do not forget to add it to path

- Launch terminal on your device and paste the code below

```
## to verify that hugo works
hugo verson
```

- After pasting the code above in the terminal, if there is an error, there has been an issue with the installation of hugo or adding it to path.

Step 2: Create a new site

- Go to a directory where your website details will be stored. 
- For example I used: C:\Users\isaac
- In the code below swap 'websitename' to the name of your website. The name that you add only applies to the name of the website folder, not the name on the internet.

```
## create a new site
hugo new site websitename

## go into the website directory
cd websitename
```

Step 3: Choose a theme from Hugo and download it

- There are countless theme that you can choose from https://themes.gohugo.io/ but for this guide I am going to use the theme named 'Blowfish'. In my opinion, this theme looks the best from the couple hundred available themes due to its never ending customizability features. 

- The following lines of code will initilize git and download the blowfish theme
```
## initilazing git
git init

##
git submodule add -b main https://github.com/nunocoracao/blowfish.git themes/blowfish
```


Step 4: Set up the configuration files for blowfish

- Open file explorer and open the file directory where your website code resides. 
!!![Image Description](Pasted%20image%2020241210103039.png)
- Open the 'themes' folder and open the theme called 'blowfish', in there copy the 'config' folder and paste it in the root directory of the website. 
 !!![Image Description](Pasted%20image%2020241210103927.png)








### 5. **Lessons Learned**

- **Patience and Research**: The importance of understanding the tools and reading documentation.
- **Experimenting with Customization**: How you learned to tweak the website to suit your needs.
- **Continuous Learning**: Emphasize how setting up this blog has been a learning process and how you plan to continue evolving it.

### 6. **Final Thoughts**

- Recap the process of setting up the blog and the key points from your article.
- Encourage readers to take on similar projects and learn from your experience.
- Mention future plans for the blog and what content readers can expect in the coming months.

### 7. **Call to Action**

- Invite readers to comment with their experiences if they’ve set up their own blogs or have questions.
- Mention subscribing to your newsletter or following for future posts.

**!!![Image Description](Pasted%20image%2020241210082422.png)**