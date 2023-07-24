from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px

today = datetime.today()
df = pd.DataFrame(
    [
        dict(
            name="a",
            start=(today + timedelta(minutes=0)),
            end=(today + timedelta(minutes=10)),
            resource="1",
        ),
        dict(
            name="b",
            start=(today + timedelta(minutes=3)),
            end=(today + timedelta(minutes=14)),
            resource="2",
        ),
        dict(
            name="c",
            start=(today + timedelta(minutes=10)),
            end=(today + timedelta(minutes=12)),
            resource="1",
        ),
        dict(
            name="d",
            start=(today + timedelta(minutes=13)),
            end=(today + timedelta(minutes=17)),
            resource="1",
        ),
    ]
)

fig = px.timeline(df, x_start="start", x_end="end", color="name", y="resource")
fig.show()
