#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def createPitch(length, width, linecolor):
    """
    Creates a football pitch.
    """

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Draw pitch outline and central line
    plt.plot([0, 0], [0, width], color=linecolor)
    plt.plot([0, length], [width, width], color=linecolor)
    plt.plot([length, length], [width, 0], color=linecolor)
    plt.plot([length, 0], [0, 0], color=linecolor)
    plt.plot([length / 2, length / 2], [0, width], color=linecolor)

    # Draw left penalty area
    plt.plot([16.5, 16.5], [(width / 2 + 20.16), (width / 2 - 20.16)], color=linecolor)
    plt.plot([0, 16.5], [(width / 2 + 20.16), (width / 2 + 20.16)], color=linecolor)
    plt.plot([16.5, 0], [(width / 2 - 20.16), (width / 2 - 20.16)], color=linecolor)

    # Draw right penalty area
    plt.plot([(length - 16.5), length],[(width / 2 + 20.16), (width / 2 + 20.16)],color=linecolor)
    plt.plot([(length - 16.5), (length - 16.5)],[(width / 2 + 20.16), (width / 2 - 20.16)],color=linecolor)
    plt.plot([(length - 16.5), length],[(width / 2 - 20.16), (width / 2 - 20.16)],color=linecolor)

    # Draw left goal area
    plt.plot([0, 5.5],[(width / 2 + 7.32 / 2 + 5.5), (width / 2 + 7.32 / 2 + 5.5)],color=linecolor)
    plt.plot([5.5, 5.5],[(width / 2 + 7.32 / 2 + 5.5), (width / 2 - 7.32 / 2 - 5.5)],color=linecolor)
    plt.plot([5.5, 0],[(width / 2 - 7.32 / 2 - 5.5), (width / 2 - 7.32 / 2 - 5.5)],color=linecolor)

    # Draw right goal area
    plt.plot([length, length - 5.5],[(width / 2 + 7.32 / 2 + 5.5), (width / 2 + 7.32 / 2 + 5.5)],color=linecolor)
    plt.plot([length - 5.5, length - 5.5],[(width / 2 + 7.32 / 2 + 5.5), width / 2 - 7.32 / 2 - 5.5],color=linecolor)
    plt.plot([length - 5.5, length],[width / 2 - 7.32 / 2 - 5.5, width / 2 - 7.32 / 2 - 5.5],color=linecolor)

    # Draw left goal 
    plt.plot([-3, 0],[(width / 2 + 7.32 / 2), (width / 2 + 7.32 / 2)],color="gray")
    plt.plot([-3, -3],[(width / 2 + 7.32 / 2), (width / 2 - 7.32 / 2)],color="gray")
    plt.plot([-3, 0],[(width / 2 - 7.32 / 2), (width / 2 - 7.32 / 2)],color="gray")

    # Draw right goal 
    plt.plot([length, length + 3],[(width / 2 + 7.32 / 2), (width / 2 + 7.32 / 2)],color="gray")
    plt.plot([length + 3, length + 3],[(width / 2 + 7.32 / 2), width / 2 - 7.32 / 2],color="gray")
    plt.plot([length + 3, length],[width / 2 - 7.32 / 2, width / 2 - 7.32 / 2],color="gray")

    # Define circles
    centreCircle = plt.Circle((length / 2, width / 2), 9.15, color=linecolor, fill=False)
    centreSpot = plt.Circle((length / 2, width / 2), 0.5, color=linecolor)
    leftPenaltySpot = plt.Circle((11, width / 2), 0.5, color=linecolor)
    rightPenaltySpot = plt.Circle((length - 11, width / 2), 0.5, color=linecolor)

    # Draw circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenaltySpot)
    ax.add_patch(rightPenaltySpot)

    # Define arcs
    leftArc = Arc(
        (11, width / 2),
        height=18.3,
        width=18.3,
        angle=0,
        theta1=308,
        theta2=52,
        color=linecolor,
    )
    rightArc = Arc(
        (length - 11, width / 2),
        height=18.3,
        width=18.3,
        angle=0,
        theta1=128,
        theta2=232,
        color=linecolor,
    )

    # Draw arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis("off")

    return fig, ax
