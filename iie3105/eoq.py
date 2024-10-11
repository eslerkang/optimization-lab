import numpy as np
from scipy import stats
import math

# 주어진 매개변수
a = 0.5094208594435883
c = 1.9562541556953779
loc = 0.9999997401710807
scale = 67.51815157840537

# 재무 정보
product_revenue = 1450  # 드럼당 수익
interest_rate = 0.10  # 연간 이자율
production_cost_fixed = 1500  # 고정 생산 비용
production_cost_variable = 1000  # 배치 크기당 변동 생산 비용
shipping_cost_truck = 15000  # 트럭당 배송 비용
truck_capacity = 200  # 트럭 용량 (드럼)
holding_cost = 100  # 드럼당 연간 재고 유지 비용
fulfillment_cost = 150  # 드럼당 고객 이행 비용

# 새로운 매개변수
capacity = 45  # 생산 용량

# 예시 값
annual_demand = 14305.5  # 연간 수요
order_cost = 1500  # 주문 비용
service_level = 0.90  # 서비스 수준


def calculate_mean_std(a, c, loc, scale):
    """일반화된 감마 분포의 평균과 표준편차 계산"""
    mean = loc + scale * math.gamma(a + 1 / c) / math.gamma(a)
    var = scale**2 * (
        math.gamma(a + 2 / c) / math.gamma(a)
        - (math.gamma(a + 1 / c) / math.gamma(a)) ** 2
    )
    std = math.sqrt(var)
    return mean, std


def calculate_eoq(annual_demand, order_cost, holding_cost):
    """EOQ 계산"""
    return math.sqrt((2 * annual_demand * order_cost) / holding_cost)


def calculate_lead_time(batch_size):
    """배치 크기에 따른 lead time 계산"""
    return 7 + batch_size / capacity


def calculate_rop(mean, std, lead_time, service_level):
    """ROP 계산"""
    safety_factor = stats.norm.ppf(service_level)
    safety_stock = safety_factor * std * math.sqrt(lead_time)
    rop = (mean * lead_time) + safety_stock
    return rop


def calculate_total_cost(Q, r, mean, std, lead_time):
    """총 비용 계산"""
    num_orders = annual_demand / Q
    production_cost = (
        production_cost_fixed + production_cost_variable * Q
    ) * num_orders

    num_trucks = math.ceil(Q / truck_capacity)
    shipping_cost = shipping_cost_truck * num_trucks * num_orders

    inventory_cost = holding_cost * (Q / 2 + r - mean * lead_time)

    stockout_prob = 1 - stats.norm.cdf(
        (r - mean * lead_time) / (std * math.sqrt(lead_time))
    )
    expected_stockout = (
        std
        * math.sqrt(lead_time)
        * stats.norm.pdf((r - mean * lead_time) / (std * math.sqrt(lead_time)))
        - (r - mean * lead_time) * stockout_prob
    )
    stockout_cost = num_orders * fulfillment_cost * expected_stockout

    total_cost = production_cost + shipping_cost + inventory_cost + stockout_cost
    return total_cost


def optimize_Q_r(mean, std):
    """Q와 r의 최적값 찾기"""
    best_Q = eoq  # EOQ를 초기값으로 사용
    best_r = rop  # 초기 ROP 값 사용
    best_cost = float("inf")

    for Q in range(int(best_Q * 0.5), int(best_Q * 1.5), 1):  # EOQ 주변 탐색
        lead_time = calculate_lead_time(Q)
        for r in range(
            int(mean * lead_time),
            int(mean * lead_time + 4 * std * math.sqrt(lead_time)),
            1,
        ):
            cost = calculate_total_cost(Q, r, mean, std, lead_time)
            if cost < best_cost:
                best_cost = cost
                best_Q = Q
                best_r = r

    return best_Q, best_r, best_cost


# 평균과 표준편차 계산
mean, std = calculate_mean_std(a, c, loc, scale)

# EOQ 계산 (초기값으로 사용)
eoq = calculate_eoq(annual_demand, order_cost, holding_cost)

# 초기 Lead time 계산
lead_time = calculate_lead_time(eoq)

# 초기 ROP 계산
rop = calculate_rop(mean, std, lead_time, service_level)

# Q,r 모델 최적화
optimal_Q, optimal_r, optimal_cost = optimize_Q_r(mean, std)

# 결과 출력
print(f"평균 일일 수요: {mean:.2f}")
print(f"일일 수요의 표준편차: {std:.2f}")
print(f"초기 EOQ: {eoq:.2f}")
print(f"초기 ROP: {rop:.2f}")
print(f"최적 주문량 (Q): {optimal_Q:.2f}")
print(f"최적 재주문점 (r): {optimal_r:.2f}")
print(f"최적 Lead Time: {calculate_lead_time(optimal_Q):.2f}")
print(f"최적 총 비용: ${optimal_cost:.2f}")
print(f"필요한 트럭 수: {math.ceil(optimal_Q / truck_capacity)}")

# 서비스 수준 계산
optimal_lead_time = calculate_lead_time(optimal_Q)
z_score = (optimal_r - mean * optimal_lead_time) / (std * math.sqrt(optimal_lead_time))
actual_service_level = stats.norm.cdf(z_score)
print(f"실제 서비스 수준: {actual_service_level:.4f}")
