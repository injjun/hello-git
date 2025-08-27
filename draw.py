import math
from typing import Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
from matplotlib import cm


def draw_circle(
    radius: float,
    center: Tuple[float, float] = (0.0, 0.0),
    color: str = "black",
    fill: bool = False,
    linewidth: float = 2.0,
    figsize: Tuple[float, float] = (4, 4),
    save: Optional[str] = None,
    show: bool = True,
    bgcolor: str = "white",
) -> plt.Figure:
    """
    Draw a circle using matplotlib.

    Args:
        radius: radius of the circle (must be > 0).
        center: (x, y) center coordinates.
        color: edge (or fill) color.
        fill: whether to fill the circle.
        linewidth: edge line width.
        figsize: figure size in inches.
        save: optional path to save the image (e.g., 'circle.png').
        show: if True, display the figure with plt.show().
        bgcolor: background color of the canvas.

    Returns:
        The matplotlib.figure.Figure object.
    """
    if radius <= 0:
        raise ValueError("radius must be greater than 0")

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(bgcolor)
    ax.set_aspect("equal")
    ax.set_facecolor(bgcolor)

    circ = patches.Circle(center, radius, edgecolor=color, facecolor=color if fill else "none", linewidth=linewidth)
    ax.add_patch(circ)

    # set limits with a little margin
    margin = max(0.1 * radius, 0.1)
    x0, y0 = center
    ax.set_xlim(x0 - radius - margin, x0 + radius + margin)
    ax.set_ylim(y0 - radius - margin, y0 + radius + margin)

    # remove axes for cleaner output
    ax.axis("off")

    if save:
        plt.savefig(save, bbox_inches="tight", facecolor=fig.get_facecolor())

    if show:
        plt.show()

    return fig


def _star_vertices(center: Tuple[float, float], outer_radius: float, inner_radius: float, points: int):
    cx, cy = center
    verts = []
    angle = math.pi / 2  # start pointing upwards
    step = math.pi / points
    for i in range(2 * points):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        verts.append((x, y))
        angle += step
    return verts


def draw_rainbow_star(
    radius: float,
    center: Tuple[float, float] = (0.0, 0.0),
    points: int = 5,
    inner_radius_ratio: float = 0.5,
    linewidth: float = 3.0,
    fill: bool = True,
    figsize: Tuple[float, float] = (6, 6),
    save: Optional[str] = None,
    show: bool = True,
    bgcolor: str = "white",
) -> plt.Figure:
    """
    Draw a star with rainbow-colored edges.

    Args:
        radius: outer radius of the star (>0).
        center: (x, y) center of the star.
        points: number of star points (integer >= 2).
        inner_radius_ratio: inner/outer radius ratio (0 < r < 1).
        linewidth: line width for edges.
        fill: whether to fill the star with a translucent color.
        figsize, save, show, bgcolor: same semantics as draw_circle.

    Returns:
        matplotlib.figure.Figure
    """
    if radius <= 0:
        raise ValueError("radius must be greater than 0")
    if points < 2 or not isinstance(points, int):
        raise ValueError("points must be an integer >= 2")
    if not (0.0 < inner_radius_ratio < 1.0):
        raise ValueError("inner_radius_ratio must be between 0 and 1")

    inner_radius = radius * inner_radius_ratio
    verts = _star_vertices(center, radius, inner_radius, points)

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(bgcolor)
    ax.set_aspect("equal")
    ax.set_facecolor(bgcolor)

    # Prepare segments for colored edges
    n = len(verts)
    segments = [ (verts[i], verts[(i + 1) % n]) for i in range(n) ]
    colors = [cm.rainbow(i / n) for i in range(n)]
    lc = LineCollection(segments, colors=colors, linewidths=linewidth, capstyle='round')
    ax.add_collection(lc)

    # Optional translucent fill (single color, so keep subtle)
    if fill:
        poly = patches.Polygon(verts, closed=True, facecolor=cm.rainbow(0.5), alpha=0.25, edgecolor='none')
        ax.add_patch(poly)

    # set limits with margin
    margin = max(0.2 * radius, 0.1)
    x0, y0 = center
    ax.set_xlim(x0 - radius - margin, x0 + radius + margin)
    ax.set_ylim(y0 - radius - margin, y0 + radius + margin)

    ax.axis("off")

    if save:
        plt.savefig(save, bbox_inches="tight", facecolor=fig.get_facecolor())

    if show:
        plt.show()

    return fig


if __name__ == "__main__":
    # 간단한 사용 예:
    # 반지름 1짜리 채워진 빨간 원을 그리고 화면에 표시하고 circle_example.png로 저장합니다.
    draw_circle(1.0, center=(0, 0), color="green", fill=True, save="circle_example.png")

    # 무지개색 별 예제: 5점 별을 그리고 rainbow_star.png로 저장합니다.
    draw_rainbow_star(1.5, center=(0, 0), points=5, inner_radius_ratio=0.5, linewidth=4, fill=True, save="rainbow_star.png")