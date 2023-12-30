<h1>ChatShop</h1>

</a>

  

<h2>

Looking for a Flawless E-Commerce Solution?

</h2>

<h2>

# Introducing ChatShop

</h2>

  

<p  >

Why Settle for Less When Our Combined AI Agents Can Offer Perfection? Discover Unparalleled E-Commerce Mastery: Our Fusion of AI Agents Delivers Flawless Execution and Exceptional Performance.

</p>

  

<p  >

<a  href="#description"><strong>Description</strong></a> ·

<a  href="#features"><strong>Features</strong></a> ·

<a  href="#mind-boggling-features"><strong>Mind-Boggling Features</strong></a> ·

<a  href="#running-locally"><strong>Running locally</strong></a> ·

<a  href="#future-scope"><strong>Future Scope</strong></a> ·

</p>

<br/>

  ## Our Motivation
  -   Managing an Online Business can be quite a hassle and services that claim to do the entire thing from end to end for you often end up charging quite a lot.
    

-   The result? Small scale businesses or individuals wishing to host their own online store front either end up paying so much money to a third party that if their business doesn't boom, they go in a spiral of losses.
    

-   Either that, or they end up wasting their own time and energy managing orders, shipments, payments and customer queries; eating up a significant chunk of their time.

## Description

  

In our cutting-edge e-commerce platform, we've integrated the power of multiple AI agents, each powered by advanced Language Learning Models (LLMs), to revolutionize and streamline user interactions. When a prompt is entered into our system, the first AI agent activates. With its LLM expertise, it swiftly determines whether the prompt is related to store operations or a customer inquiry.

  

If the prompt is store-related, a second specialized AI agent takes the helm. This agent, also equipped with LLM technology, classifies the prompt further into either an information request or a purchase query. Based on this classification, the prompt is then efficiently processed by our specialized agents who excel in database operations, ensuring accurate and prompt responses for store-related queries.

  

For customer-related prompts, the initial response is managed by a help-type AI agent. This agent, adept at resolving common customer inquiries, utilizes its LLM capabilities to provide swift assistance. However, if the query is more complex or serious, our system intelligently escalates it to a ‘contact human’ agent. This ensures that while most inquiries are resolved automatically and quickly, those requiring more nuanced attention receive the human touch they deserve.

  

Our platform's multi-layered, AI-driven approach not only boosts efficiency and accuracy but also enhances the user experience. Both store operators and customers benefit from our innovative and effective solution, tailored to meet a wide range of needs in the ever-evolving e-commerce landscape.


## Flow of Agents
  



## Implementation

https://github.com/korebhaumik/Hack_AI_Final_Submission/assets/96487647/a28657af-aa6f-43d3-bc4a-e01e07fc0289



  

This video showcases the seamless integration of multiple AI agents in our innovative e-commerce platform, demonstrating how they collaborate to revolutionize and streamline online business interactions.

  

## Features

  

-  *FetchAI uAgents*: Dynamic AI interactions

-  *Redis*: Robust, high-speed database solution

-  *OpenAI API*: Harnessing powerful language models

-  *Discord Bot*: Seamless user engagement interface

  

## Mind-Boggling Features

  
<img width="1776" alt="fetch_ai_dia" src="https://github.com/korebhaumik/Hack_AI_Final_Submission/assets/96487647/f06ab926-3341-47ae-ba61-b22f092b67a6">


1.  *Innovative Problem-Solving*: Our approach utilizes a unique blend of AI agents, each expertly tailored to address specific aspects of e-commerce challenges, ensuring comprehensive solutions.

  

2.  *Precision and Accuracy*: By combining the strengths of various AI technologies, we achieve unparalleled accuracy in operations, from customer interactions to inventory management.

  

3.  *Efficiency and Speed*: Our integrated AI agents work in concert to streamline processes, significantly reducing response times and increasing overall productivity.

  

5.  *User-Centric Design*: At the heart of our approach is a deep understanding of user needs, ensuring that every solution is not only effective but also user-friendly and intuitive.

  

6.  *Scalable Solutions*: Our AI-driven platform is built to scale, capable of handling the evolving demands of modern e-commerce with ease and agility.

  

7.  *Future-Proofing E-Commerce*: We're not just solving today's problems; we're anticipating future challenges, ensuring our clients stay ahead in a rapidly changing digital marketplace.

  

## Running locally

  

You will need to have the necessary environment variables setup in your .env file.

This include keys for your Supabase account, and Stripe account, Github Outh Client, Github Outh Secret.

bash

HOST  =

GITHUB_CLIENT_ID  =

GITHUB_CLIENT_SECRET  =



  

> Note: You should not commit your .env file or it will expose secrets that will allow others to control access to your authentication provider accounts.

  

1. Install run: pnpm i

2. Make a new .env file.

3. Populate the .env file with the necessary environment variables.

  

bash

pnpm  run  dev



  

Your app template should now be running on [localhost:5173](http://localhost:5173/).

  

## Running locally with docker

  

bash

docker  login

docker  pull  korebhaumik/mernifier-web.

docker  run  -env-file  .env  -p  3000:3000  korebhaumik/mernifier-web



  

> Note: If the docker image is not available (repo is privated), you can build it locally by running docker build -t mernifier-web . in the root directory of the project.

  
  

## Future Scope

  

-  *Fine-Tuning Language Learning Models (LLMs)*:

Our ongoing enhancements will focus on refining the precision and context-awareness of our LLMs. This will ensure a more accurate understanding and response to user prompts, elevating the effectiveness of user interactions.

  

-  *Adaptive Learning Enhancements*:

We are committed to advancing our platform's adaptive learning capabilities. This means it will continuously improve based on user interactions and feedback, allowing for more effective adaptation to changing user needs and market dynamics.

-   *Integration with Platforms like Delta V*:
    

We aim to integrate our product into a platform like Delta V that is made specifically for e- commerce platforms and has integration with agent hosting platforms like AgentVerse. This has the potential to take our product to a production level.

-   *Catering to a Wider Customer Base*:
    

In the future, we aim to add a slew of products to our database with accompanying agents for each category to provide all types of customer support. This will also have the support for multiple languages and potentially even voice for better inclusivity and a wider reach.

-   *Whatsapp Integration*:
    

While our Agent platform can only be accessed via discord currently, we aim to bring support for other platforms like Whatsapp, Telegram or even WeChat for that matter; in the future.
