import random

TARGET = "AI_RESEARCH"
GENES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        score = 0
        for expected, actual in zip(TARGET, self.chromosome):
            if expected == actual:
                score += 1
        return score

def create_random_individual():
    chrom = "".join(random.choice(GENES) for _ in range(len(TARGET)))
    return Individual(chrom)

def mutate(chromosome):
    chrom_list = list(chromosome)
    idx = random.randint(0, len(chrom_list) - 1)
    chrom_list[idx] = random.choice(GENES)
    return "".join(chrom_list)

def crossover(parent1, parent2):
    mid = len(parent1) // 2
    child_chrom = parent1[:mid] + parent2[mid:]
    return Individual(child_chrom)

if __name__ == "__main__":
    random.seed()
    population_size = 100
    generation = 1

    population = [create_random_individual() for _ in range(population_size)]

    print(f"-> 🧬 開始基因演算法研究，目標: {TARGET}\n")

    found = False
    while generation <= 1000:
        population.sort(key=lambda x: x.fitness, reverse=True)

        best = population[0]
        # 這裡修正了 f-string 的格式化寫法
        print(f"第 {generation:3} 代 | 最佳解答: {best.chromosome} | 適應度: {best.fitness}")

        if best.chromosome == TARGET:
            print(f"\n-> 🎉 成功在第 {generation} 代演化出目標解答！")
            found = True
            break

        next_generation = population[:int(population_size * 0.1)]

        while len(next_generation) < population_size:
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = crossover(parent1.chromosome, parent2.chromosome)

            if random.random() < 0.1:
                child = Individual(mutate(child.chromosome))

            next_generation.append(child)

        population = next_generation
        generation += 1

    if not found:
        print("\n-> ⚠️ 達到最大代數限制，演化停止。")

