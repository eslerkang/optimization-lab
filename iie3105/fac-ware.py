import gurobipy as gp
from gurobipy import GRB

model = gp.Model("fac-ware")

# 고객 수요 (Caplopeia, Sorange, Tyran, Entworpe, Fardo 순)
demand_c = [28611, 118732, 14211, 8750, 11465]

# 위치 인덱스 (0: Caplopeia, 1: Sorange, 2: Tyran, 3: Entworpe, 4: Fardo)
locations = range(5)
days = 365 * 2  # 2년 운영

# 비용 파라미터
fixed_factory_cost = 500_000  # 공장 고정비
variable_factory_cost = 50_000  # 공장 용량 단위당 비용
fixed_warehouse_cost = 100_000  # 창고 설치 기본 비용
sales_price = 1_450  # 제품 판매 가격

# 결정 변수 생성
x_fw = {}  # 공장에서 창고로의 물량
x_wc = {}  # 창고에서 고객으로의 물량
y_f = {}  # 공장 설치 여부
y_w = {}  # 창고 설치 여부
cap_f = {}  # 공장 용량
cap_w = {}  # 창고 용량

for f in locations:
    y_f[f] = model.addVar(vtype=GRB.BINARY, name=f"y_f_{f}")
    cap_f[f] = model.addVar(lb=0, name=f"cap_f_{f}")
    for w in locations:
        x_fw[f, w] = model.addVar(lb=0, name=f"x_fw_{f}_{w}")

for w in locations:
    y_w[w] = model.addVar(vtype=GRB.BINARY, name=f"y_w_{w}")
    for c in locations:
        x_wc[w, c] = model.addVar(lb=0, name=f"X_wc_{w}_{c}")


# 운송 비용 설정 (200개 단위)
transport_cost_fw = {}
for f in locations:
    for w in locations:
        if f == w:
            transport_cost_fw[f, w] = 15_000
        elif f != 4 and w != 4:  # 둘 다 대륙
            transport_cost_fw[f, w] = 20_000
        else:  # 섬-대륙 간
            transport_cost_fw[f, w] = 45_000

# 창고-고객 운송 비용 (개당)
transport_cost_wc = {}
for w in locations:
    for c in locations:
        if w == c:
            transport_cost_wc[w, c] = 150
        elif w != 4 and c != 4:  # 둘 다 대륙
            transport_cost_wc[w, c] = 200
        else:  # 섬-대륙 간
            transport_cost_wc[w, c] = 400

# 제약 조건
# 1. 수요 제약 (최대치)
for c in locations:
    model.addConstr(gp.quicksum(x_wc[w, c] for w in locations) <= demand_c[c])

# 1. 수요 제약 (최소치)
# for c in locations:
#     model.addConstr(gp.quicksum(x_wc[w, c] for w in locations) >= demand_c[c])


# 2. 창고 물량 균형
for w in locations:
    model.addConstr(
        gp.quicksum(x_fw[f, w] for f in locations)
        == gp.quicksum(x_wc[w, c] for c in locations)
    )

# 3. 공장 용량 제약
for f in locations:
    model.addConstr(gp.quicksum(x_fw[f, w] for w in locations) <= cap_f[f] * days)

# 5. 기존 Caplopeia 공장 용량 설정
model.addConstr(cap_f[0] >= 70.02)

# 6. 공장/창고가 설치되어야만 사용 가능
for f in locations:
    for w in locations:
        model.addConstr(x_fw[f, w] <= y_f[f] * sum(demand_c))

for w in locations:
    for c in locations:
        model.addConstr(x_wc[w, c] <= y_w[w] * sum(demand_c))


total_capa_cost = (
    # 공장 고정비 + 용량 비용
    gp.quicksum(
        fixed_factory_cost * y_f[f] + variable_factory_cost * cap_f[f]
        for f in locations
    )
    +
    # 창고 설치 및 용량 비용
    gp.quicksum(fixed_warehouse_cost * y_w[w] for w in locations)
    - 70.02 * variable_factory_cost
    - fixed_factory_cost
)

# 총 비용 제약 추가
total_ship_cost = (
    # 공장-창고 운송비
    gp.quicksum(
        transport_cost_fw[f, w] * x_fw[f, w] / 200 for f in locations for w in locations
    )
    +
    # 창고-고객 운송비
    gp.quicksum(
        transport_cost_wc[w, c] * x_wc[w, c] for w in locations for c in locations
    )
)

total_cost = total_capa_cost + total_ship_cost


model.addConstr(total_capa_cost <= 6_796_509.90)

# 목적함수: 총이익 최대화 (수익 - 비용)
obj = (
    # 판매 수익
    gp.quicksum(sales_price * x_wc[w, c] for w in locations for c in locations)
    - total_cost
)

model.setObjective(obj, GRB.MAXIMIZE)

# 최적화 실행
model.optimize()

# 결과 출력
if model.status == GRB.OPTIMAL:
    print("\n최적해를 찾았습니다!")
    print(f"총 이익: {model.objVal:,.0f}원")

    print("\n공장 설치 및 용량:")
    for f in locations:
        if y_f[f].x == 1:
            print(f"위치 {f}: 용량 = {cap_f[f].x:.1f}")

    print("\n주요 물량 흐름:")
    for f in locations:
        for w in locations:
            if x_fw[f, w].x > 0:
                print(f"공장{f} -> 창고{w}: {x_fw[f,w].x:.0f}")

    print("\n고객 배송량 (2년 총계):")
    for c in locations:
        total_delivery = sum(x_wc[w, c].x for w in locations)
        fulfillment_rate = total_delivery / (demand_c[c]) * 100
        print(f"고객{c}: {total_delivery:,.0f} ({fulfillment_rate:.2f}% 충족)")
    print(f"\n총 증설 비용: {total_capa_cost.getValue():,.0f}")
    print(f"\n총 운송 비용: {total_ship_cost.getValue():,.0f}")
    print(f"\n총 비용: {total_cost.getValue():,.0f}")
else:
    print("최적해를 찾지 못했습니다.")
