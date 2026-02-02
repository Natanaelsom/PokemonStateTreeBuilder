from typing import Dict, List, Optional
from state import State
from transition import Transition


class StateTree:
    """Classe que representa uma árvore de estados com transições."""

    def __init__(self, root_state: State):
        """
        Inicializa a árvore de estados.
        
        Args:
            root_state: Estado raiz da árvore
        """
        self.root_state = root_state
        self.states: Dict[int, State] = {root_state.id: root_state}
        self.transitions: List[Transition] = []

    def add_state(self, state: State) -> bool:
        """
        Adiciona um estado à árvore.
        
        Args:
            state: Estado a ser adicionado
            
        Returns:
            True se adicionado com sucesso, False se já existe
        """
        if state.id in self.states:
            return False
        self.states[state.id] = state
        return True

    def get_state(self, state_id: int) -> Optional[State]:
        """Obtém um estado pelo seu ID."""
        return self.states.get(state_id)

    def remove_state(self, state_id: int) -> bool:
        """
        Remove um estado da árvore (e suas transições associadas).
        
        Args:
            state_id: ID do estado a remover
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        if state_id not in self.states or state_id == self.root_state.id:
            return False
        
        # Remover todas as transições que envolvem este estado
        self.transitions = [t for t in self.transitions 
                           if t.from_state.id != state_id and t.to_state.id != state_id]
        
        del self.states[state_id]
        return True

    def add_transition(self, transition: Transition) -> bool:
        """
        Adiciona uma transição à árvore.
        
        Args:
            transition: Transição a ser adicionada
            
        Returns:
            True se adicionada com sucesso, False se estados não estão na árvore
        """
        if transition.from_state.id not in self.states or transition.to_state.id not in self.states:
            return False
        
        self.transitions.append(transition)
        return True

    def get_transitions_from(self, state_id: int) -> List[Transition]:
        """
        Obtém todas as transições que saem de um estado específico.
        
        Args:
            state_id: ID do estado de origem
            
        Returns:
            Lista de transições partindo do estado
        """
        return [t for t in self.transitions if t.from_state.id == state_id]

    def get_transitions_to(self, state_id: int) -> List[Transition]:
        """
        Obtém todas as transições que chegam a um estado específico.
        
        Args:
            state_id: ID do estado de destino
            
        Returns:
            Lista de transições chegando ao estado
        """
        return [t for t in self.transitions if t.to_state.id == state_id]

    def remove_transition(self, transition: Transition) -> bool:
        """
        Remove uma transição da árvore.
        
        Args:
            transition: Transição a remover
            
        Returns:
            True se removida com sucesso
        """
        try:
            self.transitions.remove(transition)
            return True
        except ValueError:
            return False

    def validate_probabilities(self, state_id: int) -> bool:
        """
        Valida que as probabilidades de transições saindo de um estado somam 1.0.
        
        Args:
            state_id: ID do estado a validar
            
        Returns:
            True se as probabilidades somam ~1.0, False caso contrário
        """
        transitions = self.get_transitions_from(state_id)
        if not transitions:
            return True
        
        total_prob = sum(t.probability for t in transitions)
        return abs(total_prob - 1.0) < 0.001  # Tolerância para erros de ponto flutuante

    def auto_adjust_probabilities(self, state_id: int) -> None:
        """
        Ajusta automaticamente as probabilidades das transições saindo de um estado.
        
        Se alguma transição tiver probabilidade < 1.0, as demais transições com 
        probabilidade 1.0 dividem o restante igualmente.
        
        Regra:
        - Se uma transição tem prob definida < 1.0, é mantida
        - As demais com prob = 1.0 dividem o restante (100% - prob_definidas) igualmente
        
        Args:
            state_id: ID do estado
        """
        transitions = self.get_transitions_from(state_id)
        
        if not transitions:
            return
        
        # Separar transições com probabilidade definida vs default (1.0)
        defined_transitions = [t for t in transitions if t.probability < 1.0]
        default_transitions = [t for t in transitions if t.probability == 1.0]
        
        # Se nenhuma transição tem probabilidade definida, todas recebem 1/n
        if not defined_transitions:
            equal_prob = 1.0 / len(transitions)
            for t in transitions:
                t.probability = equal_prob
            return
        
        # Se todas têm probabilidade definida, validar se soma 1.0
        if not default_transitions:
            total = sum(t.probability for t in defined_transitions)
            if abs(total - 1.0) > 0.001:
                # Normalizar se não soma exatamente 1.0
                for t in defined_transitions:
                    t.probability = t.probability / total
            return
        
        # Caso misto: ajustar as transições default
        total_defined = sum(t.probability for t in defined_transitions)
        remaining_prob = 1.0 - total_defined
        
        if remaining_prob < 0:
            # Se as definidas já ultrapassam 1.0, normalizar tudo
            for t in defined_transitions:
                t.probability = t.probability / total_defined
            for t in default_transitions:
                t.probability = 0.0
        else:
            # Dividir o restante igualmente entre as transições default
            equal_default_prob = remaining_prob / len(default_transitions)
            for t in default_transitions:
                t.probability = equal_default_prob

    def get_all_states(self) -> List[State]:
        """Retorna uma lista de todos os estados na árvore."""
        return list(self.states.values())

    def get_all_transitions(self) -> List[Transition]:
        """Retorna uma lista de todas as transições na árvore."""
        return self.transitions.copy()

    def __repr__(self) -> str:
        return f"StateTree(root='{self.root_state.name}', states={len(self.states)}, transitions={len(self.transitions)})"
