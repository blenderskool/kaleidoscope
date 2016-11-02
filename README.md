#Prism

Prism is an add-on developed for Cycles in Blender. The add-on adds two new Nodes to Materials, "Spectrum" and "Intensity", which essentially improves your workflow inside Blender when creating Materials for your objects

#Why?

The reason I created this add-on was to provide the most essential tasks needed while creating scenes in Blender. As an artist myself, I do get stuck in Colors, Lighting, and even more!
And this small package of nodes is designed to improve and fix all that. I do understand that Blender nodes can be scary sometimes, but these nodes are well designed just so that anyone can use them :)

<h1>So What Nodes are Added</h1>
While there are only 2 Nodes in the Prism add-on, both are extremely powerful, and can be customized to give results based on your liking. The Nodes that come with the add-on are:

#Spectrum:
Spectrum is a Node which allows you to generate visually appealing color schemes and palettes. It comes with the Spectrum Engine, which is designed to generate infinite color shades and palettes. But to make it even more powerful, it comes with Color rules such as Monochromatic, Analogous, Triadic, and even more. So you can select the type of Color Rule you are looking for, and let Spectrum generate the Color palette based on that rule.<br>
It also comes with Global Color Controls, to manipulate the Hue, Saturation and Value of the Palette. Since the Spectrum Node is global in a Blender scene. You can generate a new palette, and see the live changes directly. No need to update any link or material.

I have also created an online library of popular palettes. These can be easily used within the Spectrum Node

There's even more in the Spectrum Node, but I will leave that to you to check it out ;)

#Intensity:
Intensity Node is mainly designed to store predefined values for certain values of nodes in Blender. For example, the Glass IOR value, which defines the refractive index of the material, is important to be physically correct to product accurate results. So the Intensity Node is the collection of all those values. So you can browse through values such as Water, Diamond, and even more.

The two Categories which are available in the Intensity node are Glass IOR, and Blackbody. I do plan in adding more in the future :)

#Development
I have designed Prism add-on in such a way, that it can be used in any other Blender add-on also. Since the Spectrum Node only modifies an object's material, the spectrum.py file can be imported into other add-ons and used more productively. I did create a Grease Pencil Palette generator with the spectrum.py file in just few minutes.

I would be really glad to see other people use the Prism add-on in their projects, and in other add-ons too. This add-on would be constantly updated with more features and improvements :)
