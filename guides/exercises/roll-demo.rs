fn try_roll(stamina: &mut u32, cost: u32) -> bool {
    if *stamina < cost {
        return false;
    }
    *stamina -= cost;
    true
}

fn main() {
    let mut stamina = 100;
    for attempt in 1..=6 {
        let accepted = try_roll(&mut stamina, 20);
        println!("Attempt {attempt}: {accepted}, left {stamina}");
    }
}

#[cfg(test)]
mod tests {
    use super::try_roll;

    #[test]
    fn exact_cost_succeeds_then_empty_is_refused() {
        let mut stamina = 20;
        assert!(try_roll(&mut stamina, 20));
        assert_eq!(stamina, 0);
        assert!(!try_roll(&mut stamina, 20));
        assert_eq!(stamina, 0);
    }
}
