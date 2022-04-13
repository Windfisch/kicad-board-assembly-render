# KiBAR -- KiCAD Board Assembly Renderer

Yea, your PCB project is nice, but -- as always -- it's a hassle to build, especially for
beginners. If those count towards your target group, they'll be in big trouble if you can't
provide them with a nice and shiny graphical build guide, showing not only which parts to put
where, but also in what order.

I hear you whimpering _"Noooo, but rendering my board with KiCAD is painful enough, I can't be
bothered screenshotting the thing a dozen times"_, and very right you are. But fear not, KiBAR
has your back!

KiBAR takes your KiCAD PCB and a **list of build steps**, and converts them into nicely looking,
step-by-step intermediate photo renders of the assembly procedure. Fully automatic! Isn't that
great?

## Dependencies

- python-opencv (Version 4 works for me)
- KiCAD 6
- [kiauto 1.6.8](https://github.com/INTI-CMNB/KiAuto)

Note that `pcbnew_do` from kiauto is somewhat flaky, since it simulates clicking buttons in KiCAD.
Make sure that, when opening your project, no message / warning boxes or whatsoever pop up, because
they can confuse `pcbnew_do`.

## Usage

`render.py your_pcb.kicad_pcb output_directory/ outpattern width height`

- `output_directory` needs to exist. Your resulting images and any intermediate files are stored
  here
- `outpattern` can be either "`prefix%suffix`", in which case your files will be called
  `prefix01suffix` and so on, or just `prefix`.
- `width` and `height` are somewhat related to the resulting image size. Images will be slightly
  smaller though, due to window borders.

## Example output

TODO

## FAQ

- **This is _so slow_.** -- Yes. This ain't a question though.
- **Why is this so slow?** -- Because *kiauto* is simulating mouse clicks in KiCAD and has ample
  timeouts for doing so. After all, I don't care because it's still faster than doing this by hand.
