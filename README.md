<div align="center"><h1>Estimating π using Monte Calro Simulation</h1> </div>

<br>



https://user-images.githubusercontent.com/57635525/168703643-4fcc966e-c095-41e2-8b3e-ed39f3b7883d.mp4



<br>

<h2>Installation</h2>

```bash
git clone https://github.com/CodePleaseRun/pi-estimation.git
cd pi-estimation
```

**Dependencies:**

- `matplotlib`
- `numpy`

<br>
<h2>Usage</h2>

```python
python estimatepi.py
```

- Number of points simulated can be changed by changing the value of `POINTS` global variable
- `POINTS_PER_FRAME` decides how many points will be animated in each fram, i.e., how many points will be aimated everytime `update_func()` is called
- Setting `POINTS_PER_FRAME` to a high value will animate graph faster but it will also make the animating "choppy" or "laggy"
- Restrictions on `POINT_PER_FRAME`:
  - `POINT_PER_FRAME` < `POINTS` < `POINTS`
  - `POINTS_PER_FRAME` must be a factor of `POINTS`

<br>

<h2>Licence</h2>
MIT
