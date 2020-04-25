# Kaleidoscope addon for Blender

Kaleidoscope is an add-on developed for Cycles and Eevee in Blender 2.8 and above. The add-on adds two new nodes, **Spectrum** and **Intensity**, which essentially improves your workflow inside Blender when creating materials.

## Why?

The reason I created this add-on was to provide other essential nodes needed while working in Blender. As an artist myself, I sometimes get stuck in colors, lighting, and even more!
And this small package of nodes will help in improving that. I do understand that Blender nodes can be scary sometimes, but these nodes are well designed so that anyone can use them.

## So What Nodes come with Kaleidoscope?
While there are 2 Nodes in the Kaleidoscope add-on, both are powerful and can be customized to give results based on your needs. The nodes that come with the add-on are:

### Spectrum
Spectrum is a node that allows you to generate visually appealing color schemes and palettes. It comes with the Spectrum Engine, which can generate infinite color shades and palettes. But to make it even more powerful, it comes with color rules such as Monochromatic, Analogous, Triadic, and even more. You can select the color rule you are looking for, and let Spectrum generate the color palette based on that rule.  
It also comes with global color controls, to manipulate the Hue, Saturation, and Value of the entire palette. Since Spectrum is a global node in Blender, you can generate a new palette, and see the live changes directly in the entire scene. No need to update any link or material.

I have also created an online library of popular palettes. You can use them directly within the Spectrum node.
Along with this, Spectrum has an option to fetch beautiful palettes from [COLOURLovers](http://www.colorlovers.com)

There's even more in the Spectrum node, but I will leave that to you to check it out 😉

### Intensity
The Intensity node is mainly designed to store predefined values for certain constants in Blender. For example, the Glass IOR value which defines the refractive index of the material is important to create physically accurate materials. The Intensity node is the collection of all those values. You can browse through values such as Water, Diamond, and even more.

The two categories which are available in the Intensity node are Glass IOR and Blackbody.

## Development
I would be glad to see other people use the Kaleidoscope add-on in their projects. I would try my best to update with more features and improvements :)

## A lookback from 2020
The code for this addon is quite messy since back then when I originally developed this addon, I was new to programming in Python and didn't pay attention to how the code was structured - it was mainly written to get the desired functionality.

Today after 4 years since this addon's release, my skills have improved considerably and **there are parts of this addon that I would develop in a completely different way compared to what I did back then**. Still, I would be glad if this addon helped artists throughout these years, and at the end this project itself was a great learning experience for me 😇

## Credits
These tools have inspired and helped me in making this add-on for Blender:
- [COLOURLovers](https://www.colorlovers.com)
- [Coolors](https://www.coolors.co)
- [Adobe Color CC](https://color.adobe.com)

# License
Kaleidoscope is [GPL Licensed](https://github.com/blenderskool/kaleidoscope/blob/master/LICENSE)