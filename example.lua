-- Advanced Game Character System
-- Example Lua script for Lua Obfuscator testing

local Character = {}
Character.__index = Character

-- Create a new character instance
function Character.new(name, health, mana)
    local self = setmetatable({}, Character)
    
    -- Character attributes
    self.name = name or "Unnamed Hero"
    self.health = health or 100
    self.maxHealth = health or 100
    self.mana = mana or 50
    self.maxMana = mana or 50
    self.level = 1
    self.experience = 0
    self.inventory = {}
    self.skills = {}
    self.status = "normal"
    
    return self
end

-- Calculate damage based on attack power and level
function Character:calculateDamage(baseAttack, targetDefense)
    -- Calculate base damage
    local attackBonus = self.level * 5
    local baseDamage = baseAttack + attackBonus - targetDefense
    
    -- Add random variance (90-110%)
    local variance = math.random(90, 110) / 100
    local finalDamage = math.max(1, baseDamage * variance)
    
    return finalDamage
end

-- Apply damage to the character
function Character:takeDamage(damage)
    local actualDamage = math.max(1, damage)
    self.health = self.health - actualDamage
    
    if self.health <= 0 then
        self.health = 0
        self.status = "dead"
        return false
    end
    
    return true
end

-- Restore health
function Character:heal(amount)
    local healAmount = math.min(amount, self.maxHealth - self.health)
    self.health = self.health + healAmount
    return healAmount
end

-- Cast a spell (requires mana)
function Character:castSpell(spellName, manaCost, damage)
    if self.mana < manaCost then
        return false, "Not enough mana"
    end
    
    self.mana = self.mana - manaCost
    
    local spellEffects = {
        ["Fireball"] = function() return damage + self.level * 10 end,
        ["Heal"] = function() self:heal(30); return 30 end,
        ["Lightning"] = function() return damage * 1.5 end,
        ["Frost"] = function() return damage * 0.8 end,
    }
    
    if spellEffects[spellName] then
        local result = spellEffects[spellName]()
        return true, result
    else
        return false, "Unknown spell"
    end
end

-- Gain experience and level up
function Character:gainExperience(amount)
    self.experience = self.experience + amount
    
    local expNeeded = self.level * 100
    if self.experience >= expNeeded then
        self.level = self.level + 1
        self.maxHealth = self.maxHealth + 10
        self.health = self.maxHealth
        self.maxMana = self.maxMana + 5
        self.mana = self.maxMana
        return true
    end
    
    return false
end

-- Add item to inventory
function Character:addItem(itemName, quantity)
    quantity = quantity or 1
    
    if self.inventory[itemName] then
        self.inventory[itemName] = self.inventory[itemName] + quantity
    else
        self.inventory[itemName] = quantity
    end
end

-- Use item from inventory
function Character:useItem(itemName)
    if not self.inventory[itemName] or self.inventory[itemName] <= 0 then
        return false
    end
    
    local itemEffects = {
        ["Health Potion"] = function() self:heal(50) end,
        ["Mana Potion"] = function() self.mana = self.maxMana end,
        ["Antidote"] = function() self.status = "normal" end,
    }
    
    if itemEffects[itemName] then
        itemEffects[itemName]()
        self.inventory[itemName] = self.inventory[itemName] - 1
        return true
    end
    
    return false
end

-- Learn a new skill
function Character:learnSkill(skillName, proficiency)
    proficiency = proficiency or 1
    
    if not self.skills[skillName] then
        self.skills[skillName] = proficiency
    else
        self.skills[skillName] = self.skills[skillName] + proficiency
    end
end

-- Get character information
function Character:getInfo()
    local info = {
        name = self.name,
        level = self.level,
        health = self.health,
        maxHealth = self.maxHealth,
        mana = self.mana,
        maxMana = self.maxMana,
        experience = self.experience,
        status = self.status,
        inventory = self.inventory,
        skills = self.skills,
    }
    return info
end

-- Print character stats
function Character:printStats()
    print(string.format("=== %s ===", self.name))
    print(string.format("Level: %d", self.level))
    print(string.format("Health: %d/%d", self.health, self.maxHealth))
    print(string.format("Mana: %d/%d", self.mana, self.maxMana))
    print(string.format("Experience: %d", self.experience))
    print(string.format("Status: %s", self.status))
end

-- Main game loop example
local function main()
    print("=== Lua Obfuscator Test: Game Demo ===\n")
    
    -- Create player and enemy
    local player = Character.new("Adventurer", 100, 50)
    local enemy = Character.new("Dragon", 150, 0)
    
    print("Player created: " .. player.name)
    print("Enemy spawned: " .. enemy.name .. "\n")
    
    -- Combat loop
    local turn = 1
    while player.health > 0 and enemy.health > 0 and turn <= 10 do
        print(string.format("--- Turn %d ---", turn))
        
        -- Player attacks
        local playerDamage = player:calculateDamage(20, 5)
        enemy:takeDamage(playerDamage)
        print(string.format("Player deals %.1f damage. Enemy HP: %d", playerDamage, enemy.health))
        
        if enemy.health <= 0 then break end
        
        -- Enemy attacks
        local enemyDamage = enemy:calculateDamage(25, 3)
        player:takeDamage(enemyDamage)
        print(string.format("Enemy deals %.1f damage. Player HP: %d", enemyDamage, player.health))
        
        -- Player casts spell occasionally
        if turn % 3 == 0 and player.mana >= 10 then
            local success, result = player:castSpell("Fireball", 10, 30)
            if success then
                enemy:takeDamage(result)
                print(string.format("Player casts Fireball for %.1f damage!", result))
            end
        end
        
        print("")
        turn = turn + 1
    end
    
    -- Print results
    print("\n=== BATTLE RESULTS ===")
    player:printStats()
    print("")
    enemy:printStats()
    
    if player.health > 0 then
        print("\n✓ Player Wins!")
        player:gainExperience(100)
    else
        print("\n✗ Player Defeated!")
    end
end

-- Run the game
main()
