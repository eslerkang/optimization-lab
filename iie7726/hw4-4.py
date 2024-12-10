import gurobipy as gp
from gurobipy import GRB


def solve_gap():
    try:
        # 모델 생성
        m = gp.Model("GAP")

        # 데이터 설정
        agents = range(3)  # i = 1,2,3
        tasks = range(2)  # j = 1,2

        # 비용 행렬 (cij)
        c = [[20, 16], [15, 19], [19, 14]]

        # 자원 사용량 행렬 (aij)
        a = [[5, 7], [3, 8], [2, 10]]

        # 용량 제한 (bj)
        b = [6, 21]

        # 결정 변수 생성
        x = m.addVars(agents, tasks, vtype=GRB.BINARY, name="x")

        # 목적함수 설정
        m.setObjective(
            gp.quicksum(c[i][j] * x[i, j] for i in agents for j in tasks), GRB.MAXIMIZE
        )

        # 제약조건 1: 각 작업은 정확히 하나의 에이전트에 할당
        for i in agents:
            m.addConstr(gp.quicksum(x[i, j] for j in tasks) == 1)

        # 제약조건 2: 자원 용량 제한
        for j in tasks:
            m.addConstr(gp.quicksum(a[i][j] * x[i, j] for i in agents) <= b[j])

        # 모델 최적화
        m.optimize()

        # 결과 출력
        print("\n아따 행님!!!! 최적해를 찾았습니다요!!!!!\n")
        print(f"최적값: {m.objVal}")
        print("\n최적 할당:")
        for i in agents:
            for j in tasks:
                if x[i, j].x > 0.5:  # 이진변수의 반올림 오차 처리
                    print(f"작업 {i+1} → 자원 {j+1}")

        # 제약조건 검증
        print("\n제약조건 검증:")
        print("1. 할당 제약:")
        for i in agents:
            sum_row = sum(x[i, j].x for j in tasks)
            print(f"   작업 {i+1}: {sum_row:.1f}")

        print("\n2. 용량 제약:")
        for j in tasks:
            used_capacity = sum(a[i][j] * x[i, j].x for i in agents)
            print(f"   자원 {j+1}: {used_capacity:.1f} <= {b[j]}")

    except gp.GurobiError as e:
        print(f"에러 발생: {e}")


if __name__ == "__main__":
    solve_gap()
