# Gurobi 최적화 라이브러리 임포트
import gurobipy as gp
from gurobipy import GRB

# 최적화 모델 생성
model = gp.Model("fac-ware")

# 각 도시별 연간 수요량 설정 (단위: 개)
demand_c = [28611, 118732, 14211, 8750, 11465]

# 도시 위치 인덱스 정의
locations = range(5)  # 0: Caplopeia, 1: Sorange, 2: Tyran, 3: Entworpe, 4: Fardo
periods = 4  # 2년을 4분기로 나눔
period_days = 365 * 2 / periods  # 분기당 일수 계산

# 비용 관련 상수 정의
fixed_factory_cost = 500_000  # 공장 설립 고정비용 (원)
variable_factory_cost = 50_000  # 공장 용량 단위당 비용 (원/단위)
fixed_warehouse_cost = 100_000  # 창고 설립 기본 비용 (원)
sales_price = 1_450  # 제품 단위당 판매 가격 (원)

# 의사결정 변수 초기화
x_fw = {}  # 공장에서 창고로의 운송량 (단위: 개)
x_wc = {}  # 창고에서 고객으로의 운송량 (단위: 개)
y_f = {}  # 공장 설치 여부 (1: 설치, 0: 미설치)
y_w = {}  # 창고 설치 여부 (1: 설치, 0: 미설치)
cap_f = {}  # 공장 생산 용량 (단위: 개/일)

# 각 기간별, 위치별 의사결정 변수 생성
for t in range(periods):
    for f in locations:
        y_f[f, t] = model.addVar(vtype=GRB.BINARY, name=f"y_f_{f}_{t}")  # 이진변수
        cap_f[f, t] = model.addVar(lb=0, name=f"cap_f_{f}_{t}")  # 음이 아닌 실수
        for w in locations:
            x_fw[f, w, t] = model.addVar(
                lb=0, name=f"x_fw_{f}_{w}_{t}"
            )  # 음이 아닌 실수

    for w in locations:
        y_w[w, t] = model.addVar(vtype=GRB.BINARY, name=f"y_w_{w}_{t}")  # 이진변수
        for c in locations:
            x_wc[w, c, t] = model.addVar(
                lb=0, name=f"x_wc_{w}_{c}_{t}"
            )  # 음이 아닌 실수

# 공장-창고 간 운송 비용 설정 (200개 단위당 비용, 원)
transport_cost_fw = {}
for f in locations:
    for w in locations:
        if f == w:  # 같은 도시 내 운송
            transport_cost_fw[f, w] = 15_000
        elif f != 4 and w != 4:  # 대륙 내 도시 간 운송
            transport_cost_fw[f, w] = 20_000
        else:  # 대륙-섬 간 운송
            transport_cost_fw[f, w] = 45_000

# 창고-고객 간 운송 비용 설정 (개당 비용, 원)
transport_cost_wc = {}
for w in locations:
    for c in locations:
        if w == c:  # 같은 도시 내 운송
            transport_cost_wc[w, c] = 150
        elif w != 4 and c != 4:  # 대륙 내 도시 간 운송
            transport_cost_wc[w, c] = 200
        else:  # 대륙-섬 간 운송
            transport_cost_wc[w, c] = 400

# 제약조건 설정
# 1. 각 고객의 분기별 수요량을 초과하지 않도록 제한
for t in range(periods):
    for c in locations:
        model.addConstr(
            gp.quicksum(x_wc[w, c, t] for w in locations) <= demand_c[c] / periods
        )

# 2. 각 창고의 입고량과 출고량이 균형을 이루도록 제한
for t in range(periods):
    for w in locations:
        model.addConstr(
            gp.quicksum(x_fw[f, w, t] for f in locations)
            == gp.quicksum(x_wc[w, c, t] for c in locations)
        )

# 3. 각 공장의 생산량이 설정된 용량을 초과하지 않도록 제한
for t in range(periods):
    for f in locations:
        model.addConstr(
            gp.quicksum(x_fw[f, w, t] for w in locations) <= cap_f[f, t] * period_days
        )

# 4. Caplopeia 공장(0번)의 최소 용량 설정
for t in range(periods):
    model.addConstr(cap_f[0, t] >= 70.02)

# 5. 공장 용량과 설치 여부의 시간적 연속성 보장
for t in range(1, periods):
    for f in locations:
        model.addConstr(cap_f[f, t] >= cap_f[f, t - 1])  # 용량은 감소할 수 없음
        model.addConstr(y_f[f, t] >= y_f[f, t - 1])  # 한번 설치된 공장은 폐쇄 불가
    for w in locations:
        model.addConstr(y_w[w, t] >= y_w[w, t - 1])  # 한번 설치된 창고는 폐쇄 불가

# 6. 설치된 시설만 사용 가능하도록 제한
for t in range(periods):
    for f in locations:
        for w in locations:
            model.addConstr(x_fw[f, w, t] <= y_f[f, t] * sum(demand_c) / periods)

    for w in locations:
        for c in locations:
            model.addConstr(x_wc[w, c, t] <= y_w[w, t] * sum(demand_c) / periods)

# 7. 현금 흐름 관련 제약조건
cumulative_profit = {}
for t in range(periods):
    # 매출액 계산
    period_revenue = gp.quicksum(
        sales_price * x_wc[w, c, t] for w in locations for c in locations
    )

    # 비용 계산
    period_cost = (
        # 공장 관련 비용 (신규 설치 비용 + 용량 증설 비용)
        gp.quicksum(
            fixed_factory_cost * (y_f[f, t] - (y_f[f, t - 1] if t > 0 else 0))
            + variable_factory_cost * (cap_f[f, t] - (cap_f[f, t - 1] if t > 0 else 0))
            for f in locations
        )
        # 창고 신규 설치 비용
        + gp.quicksum(
            fixed_warehouse_cost * (y_w[w, t] - (y_w[w, t - 1] if t > 0 else 0))
            for w in locations
        )
        # 공장-창고 간 운송비
        + gp.quicksum(
            transport_cost_fw[f, w] * x_fw[f, w, t] / 200
            for f in locations
            for w in locations
        )
        # 창고-고객 간 운송비
        + gp.quicksum(
            transport_cost_wc[w, c] * x_wc[w, c, t]
            for w in locations
            for c in locations
        )
    )

    # 누적 이익 계산
    if t == 0:
        cumulative_profit[t] = period_revenue - period_cost
        # 초기 투자 예산 제약
        model.addConstr(period_cost <= 6_796_509.90)
    else:
        cumulative_profit[t] = cumulative_profit[t - 1] + period_revenue - period_cost

    # 각 기간의 누적 이익이 양수여야 함
    model.addConstr(cumulative_profit[t] >= 0)

# 목적함수: 마지막 기간의 누적 이익 최대화
model.setObjective(cumulative_profit[periods - 1], GRB.MAXIMIZE)

# 최적화 실행
model.optimize()

# 최적화 결과 출력
if model.status == GRB.OPTIMAL:
    print("\n최적해를 찾았습니다!")
    print(f"총 누적 이익: {model.objVal:,.0f}원")

    # 공장 설치 및 용량 출력
    print("\n기간별 공장 설치 및 용량:")
    for t in range(periods):
        print(f"\n[기간 {t+1}]")
        for f in locations:
            if y_f[f, t].x > 0.5:
                print(f"위치 {f}: 용량 = {cap_f[f,t].x:.1f}")

    # 물량 흐름 출력
    print("\n기간별 주요 물량 흐름:")
    for t in range(periods):
        print(f"\n[기간 {t+1}]")
        for f in locations:
            for w in locations:
                if x_fw[f, w, t].x > 0:
                    print(f"공장{f} -> 창고{w}: {x_fw[f,w,t].x:.0f}")

    # 고객 배송량 및 수요 충족률 출력
    print("\n기간별 고객 배송량:")
    for t in range(periods):
        print(f"\n[기간 {t+1}]")
        for c in locations:
            total_delivery = sum(x_wc[w, c, t].x for w in locations)
            fulfillment_rate = total_delivery / (demand_c[c] / periods) * 100
            print(f"고객{c}: {total_delivery:,.0f} ({fulfillment_rate:.2f}% 충족)")

    # 기간별 현금 흐름 출력
    print("\n기간별 현금 흐름:")
    for t in range(periods):
        print(f"기간 {t+1}: {cumulative_profit[t].getValue():,.0f}원")

else:
    print("최적해를 찾지 못했습니다.")
